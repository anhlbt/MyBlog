import base64
from datetime import datetime, timedelta, date
from hashlib import md5
import json
import jwt
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for, current_app
from app.extensions import db
from app.utils.elasticsearch import add_to_index, remove_from_index, query_index, es_highlight
from sqlalchemy.ext import mutable
from sqlalchemy.dialects import postgresql

class SearchableMixin(object):
    @classmethod
    def search(cls, query, page, per_page, ids=None):
        total, hits, highlights = query_index(cls.__tablename__, query, page, per_page, ids)

        if total == 0:
            return 0, cls.query.filter_by(id=0)  # If there is no match for the search term, deliberately return empty BaseQuery

        hit_ids = []  # Matched records, id list
        when = []
        for i in range(len(hits)):
            hit_ids.append(hits[i][0])
            when.append((hits[i][0], i))
        # Convert the hit_ids list into BaseQuery corresponding to the sort order (ES search score is the highest), please refer to: https://stackoverflow.com/questions/6332043/sql-order-by-multiple-values-in-specific-order/6332081#6332081
        hits_basequery = cls.query.filter(cls.id.in_(hit_ids)).order_by(db.case(when, value=cls.id))
        # Traverse BaseQuery again, highlight the keyword in the field value to be searched
        for obj in hits_basequery:
            for field, need_highlight in obj.__searchable__:
                if need_highlight:  # Only fields set to True will highlight keywords
                    source = getattr(obj, field)  # Original field value
                    highlight_source = es_highlight(source, highlights)  # Field value after keyword highlighting
                    setattr(obj, field, highlight_source)

        return total, hits_basequery

    @classmethod
    def receive_after_insert(cls, mapper, connection, target):
        '''Monitor SQLAlchemy'after_insert' event
        Please refer to: https://docs.sqlalchemy.org/en/13/orm/events.html#mapper-events'''
        add_to_index(target.__tablename__, target)

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'update': list(session.dirty)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def receive_after_delete(cls, mapper, connection, target):
        '''Listen for SQLAlchemy'after_delete' event'''
        remove_from_index(target.__tablename__, target)

    @classmethod
    def reindex(cls):
        '''Refresh the index of all data in the specified data mode'''
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        # If there are currently no resources, or the front-end requested page is out of bounds, a 404 error will be thrown
        # Automatically processed by @bp.app_errorhandler(404), that is, in response to JSON data: {error: "Not Found"}
        resources = query.paginate(page, per_page)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


# Follow others
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('timestamp', db.DateTime, default=datetime.utcnow)
)

comments_likes = db.Table(
    'comments_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('comment_id', db.Integer, db.ForeignKey('comments.id')),
    db.Column('timestamp', db.DateTime, default=datetime.utcnow)
)


blacklist = db.Table(
    'blacklist',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('block_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('timestamp', db.DateTime, default=datetime.utcnow)
)


posts_likes = db.Table(
    'posts_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('timestamp', db.DateTime, default=datetime.utcnow)
)

properties_likes = db.Table(
    'properties_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('property_id', db.Integer, db.ForeignKey('properties.id')),
    db.Column('timestamp', db.DateTime, default=datetime.utcnow)
)


class Permission:
    '''Various operations in authorization authentication correspond to binary bits, such as
    FOLLOW: 0b00000001, converted to hexadecimal to 0x01
    COMMENT: 0b00000010, converted to hexadecimal to 0x02
    WRITE: 0b00000100, converted to hexadecimal to 0x04
    ...
    ADMIN: 0b10000000, converted to hexadecimal to 0x80

    The 4th, 5th, 6th, and 7th binary bits are reserved in the middle to prepare for the subsequent increase of operation authority
    '''
    # Follow the permissions of other users
    FOLLOW = 0x01
    # Permission to post comments, comment likes and dislikes
    COMMENT = 0x02
    # Permission to write articles
    WRITE = 0x04
    # Manage website permissions (corresponding to administrator roles)
    ADMIN = 0x80


class Role(PaginatedAPIMixin, db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))  # Role Name
    default = db.Column(db.Boolean, default=False, index=True)  # When adding a new user, whether to assign the current role as the default role to the new user
    permissions = db.Column(db.Integer)  # The permissions that the role has, each operation corresponds to a binary bit, and the bit that can perform a certain operation is set to 1
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        '''When the application is deployed, you should actively execute this function and add the following roles
        Note: Users who are not logged in can browse, but cannot comment or like, etc.
        shutup: 0b0000 0000 (0x00) The user is shut in a small black room and all permissions are withdrawn
        reader: 0b0000 0011 (0x03) Readers, can follow others, comment and like, but cannot publish articles
        author: 0b0000 0111 (0x07) Author, can follow others, comment and like, publish articles
        administrator: 0b1000 0111 (0x87) Super administrator, with all rights

        In the future, if you want to add a new role, or modify the permissions of a role, modify the roles array, and then run the function
        '''
        roles = {
            'shutup': ('Little Black House', ()),
            'reader': ('Reader', (Permission.FOLLOW, Permission.COMMENT)),
            'author': ('Author', (Permission.FOLLOW, Permission.COMMENT, Permission.WRITE)),
            'administrator': ('Administrator', (Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.ADMIN)),
        }
        default_role = 'reader'
        for r in roles:  # r 是字典的键
            role = Role.query.filter_by(slug=r).first()
            if role is None:
                role = Role(slug=r, name=roles[r][0])
            role.reset_permissions()
            for perm in roles[r][1]:
                role.add_permission(perm)
            role.default = (role.slug == default_role)
            db.session.add(role)
        db.session.commit()

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def get_permissions(self):
        '''Get a list of specific operation permissions of the role'''
        p = [(Permission.FOLLOW, 'follow'), (Permission.COMMENT, 'comment'), (Permission.WRITE, 'write'), (Permission.ADMIN, 'admin')]
        #Filter out without permission. Note that you cannot use for loops, because deleting elements when traversing the list may not result in what you want, reference: : https://segmentfault.com/a/1190000007214571
        new_p = filter(lambda x: self.has_permission(x[0]), p)
        return ','.join([x[1] for x in new_p])  #Use commas to splice into str

    def to_dict(self):
        data = {
            'id': self.id,
            'slug': self.slug,
            'name': self.name,
            'default': self.default,
            'permissions': self.permissions,
            '_links': {
                'self': url_for('api.get_role', id=self.id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['slug', 'name', 'permissions']:
            if field in data:
                setattr(self, field, data[field])

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(PaginatedAPIMixin, db.Model):
    # Set the database table name, the foreign key user_id in the Post model will reference users.id
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # Do not save original password
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    image = db.Column(db.String(128), nullable=True)#anhlbt
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    # Backreference, directly query all blog posts of the current user; at the same time, there will be an author attribute in the Post instance
    # cascade is used for cascade deletion. When a user is deleted, all posts under the user will be cascade deleted
    posts = db.relationship('Post', backref='author', lazy='dynamic',
                            cascade='all, delete-orphan')
    properties = db.relationship('Property', backref='author', lazy='dynamic',
                            cascade='all, delete-orphan')

    # followeds is a list of users followed by this user
    # followers is the user's follower list
    followeds = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    # List of comments posted by users
    comments = db.relationship('Comment', backref='author', lazy='dynamic',
                               cascade='all, delete-orphan')
    # The last time the user viewed the received comments page, used to determine which received comments are new
    last_recived_comments_read_time = db.Column(db.DateTime)
    # The time the user last viewed the user’s fan page, used to determine which fans are new
    last_follows_read_time = db.Column(db.DateTime)
    # Last time the user viewed the article received and was liked the page time, used to determine which likes are new
    last_posts_likes_read_time = db.Column(db.DateTime)
    last_properties_likes_read_time = db.Column(db.DateTime)
    # The last time the user viewed the comments received and liked the page time, used to determine which of the likes are new
    last_comments_likes_read_time = db.Column(db.DateTime)
    # The last time the user viewed the blog page of the person he followed, used to determine which articles are new
    last_followeds_posts_read_time = db.Column(db.DateTime)
    # User notification
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic', cascade='all, delete-orphan')
    # Private messages sent by users
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id',
                                    backref='sender', lazy='dynamic',
                                    cascade='all, delete-orphan')
    # Private messages received by users
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic',
                                        cascade='all, delete-orphan')
    # The last time the user viewed the private message
    last_messages_read_time = db.Column(db.DateTime)
    # Harasser (a hacked person)
    # sufferers victim
    harassers = db.relationship(
        'User', secondary=blacklist,
        primaryjoin=(blacklist.c.user_id == id),
        secondaryjoin=(blacklist.c.block_id == id),
        backref=db.backref('sufferers', lazy='dynamic'), lazy='dynamic')
    #After user registration, you need to confirm the email
    confirmed = db.Column(db.Boolean, default=False)
    # The role the user belongs to
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # User's RQ background task
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    def set_password(self, password):
        '''Set user password and save as Hash value'''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''Verify that the password matches the saved Hash value'''
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        '''profile picture'''
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'location': self.location,
            'about_me': self.about_me,
            'image':self.image,
            'member_since': self.member_since.isoformat() + 'Z',
            'last_seen': self.last_seen.isoformat() + 'Z',
            'followeds_count': self.followeds.count(),
            'followers_count': self.followers.count(),
            'posts_count': self.posts.count(),
            'followeds_posts_count': self.followeds_posts().count(),
            'properties_count': self.properties.count(),
            # 'followeds_properties_count': self.followeds_properties().count(),
            'comments_count': self.comments.count(),
            'confirmed': self.confirmed,
            'role_id': self.role_id,
            'role_name': Role.query.get_or_404(self.role_id).name,
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'avatar': self.avatar(128),
                'followeds': url_for('api.get_followeds', id=self.id),
                'followers': url_for('api.get_followers', id=self.id),
                'posts': url_for('api.get_user_posts', id=self.id),
                'properties': url_for('api.get_user_properties', id=self.id),
                'followeds_posts': url_for('api.get_user_followeds_posts', id=self.id),
                'comments': url_for('api.get_user_comments', id=self.id),
                'role': url_for('api.get_role', id=self.role_id)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'name', 'location', 'about_me', 'confirmed', 'role_id']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])
            # 新建用户时，给用户自动分配角色
            if self.role is None:
                if self.email in current_app.config['ADMINS']:
                    self.role = Role.query.filter_by(slug='administrator').first()
                else:
                    self.role = Role.query.filter_by(default=True).first()

    def ping(self):
        '''Update user's last access time'''
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def get_jwt(self, expires_in=3600):
        '''After the user logs in, a valid JWT is issued'''
        now = datetime.utcnow()
        payload = {
            'user_id': self.id,
            'confirmed': self.confirmed,
            'user_name': self.name if self.name else self.username,
            'user_avatar': base64.b64encode(self.avatar(24).
                                            encode('utf-8')).decode('utf-8'),
            'permissions': self.role.get_permissions(),
            'exp': now + timedelta(seconds=expires_in),
            'iat': now
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_jwt(token):
        '''verify the validity of the JWT'''
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
        except (jwt.exceptions.ExpiredSignatureError,
                jwt.exceptions.InvalidSignatureError,
                jwt.exceptions.DecodeError) as e:
            # Token过期，或被人修改，那么签名验证也会失败
            return None
        return User.query.get(payload.get('user_id'))

    def is_following(self, user):
        '''Determine whether the current user has paid attention to the user object user, \
            if it is concerned, the left side of the following expression is 1, \
                otherwise it is 0'''
        return self.followeds.filter(
            followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        '''The current user starts to pay attention to the user object user'''
        if not self.is_following(user):
            self.followeds.append(user)

    def unfollow(self, user):
        '''The current user unfollows the user object user'''
        if self.is_following(user):
            self.followeds.remove(user)

    def followeds_posts(self):
        '''Get a list of all blogs of the current user's followers'''
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.author_id)).filter(
                followers.c.follower_id == self.id)
        # Contains the current user’s own blog list
        # own = Post.query.filter_by(user_id=self.id)
        # return followed.union(own).order_by(Post.timestamp.desc())
        return followed.order_by(Post.timestamp.desc())

    def add_notification(self, name, data):
        '''Add notifications to user instance objects'''
        # 如果具有相同名称的通知已存在，则先删除该通知
        self.notifications.filter_by(name=name).delete()
        # 为用户添加通知，写入数据库
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n

    def new_recived_comments(self):
        '''Count of new comments received by users
        include:
        1. New comments added under all posts of the user
        2. User comments (or descendants below) were replied
        '''
        last_read_time = self.last_recived_comments_read_time or datetime(1900, 1, 1)
        # All articles posted by users
        user_posts_ids = [post.id for post in self.posts.all()]
        # The new comment below the user post, that is, the post_id of the comment is in the user_posts_ids collection, and the author of the comment is not yourself (the author of the post)        
        q1 = set(Comment.query.filter(Comment.post_id.in_(user_posts_ids), Comment.author != self).all())

        # The user’s comment was replied to, find all the descendants of each user’s comment
        q2 = set()
        for c in self.comments:
            q2 = q2 | c.get_descendants()
        q2 = q2 - set(self.comments.all())  # Excluding the children and grandchildren, the users posted by themselves (because it is a multi-level comment, the user may also build a building in the children and grandchildren), and there is no need to notify if you reply by yourself
        #The total set of comments received by users is the union of q1 and q2
        recived_comments = q1 | q2
        # Finally, filter out the comments before last_read_time
        return len([c for c in recived_comments if c.timestamp > last_read_time])

    def new_follows(self):
        '''User's new fan count'''
        last_read_time = self.last_follows_read_time or datetime(1900, 1, 1)
        return self.followers.filter(followers.c.timestamp > last_read_time).count()

    def new_comments_likes(self):
        '''Count of new comments received by users'''
        last_read_time = self.last_comments_likes_read_time or datetime(1900, 1, 1)
        # Among all the comments posted by the current user, which ones are liked
        comments = self.comments.join(comments_likes).all()
        # New like record count
        new_likes_count = 0
        for c in comments:
            # Time to get likes
            for u in c.likers:
                if u != self:  # Users who like their own comments do not need to be notified
                    res = db.engine.execute("select * from comments_likes where user_id={} and comment_id={}".format(u.id, c.id))
                    timestamp = datetime.strptime(str(list(res)[0][2]), '%Y-%m-%d %H:%M:%S.%f') #add str
                    # Determine whether this like record is new
                    if timestamp > last_read_time:
                        new_likes_count += 1
        return new_likes_count

    def new_followeds_posts(self):
        '''Count of newly published articles by people that the user follows'''
        last_read_time = self.last_followeds_posts_read_time or datetime(1900, 1, 1)
        return self.followeds_posts().filter(Post.timestamp > last_read_time).count()

    def new_recived_messages(self):
        '''User unread private messages count'''
        last_read_time = self.last_messages_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def is_blocking(self, user):
        '''Determine whether the current user has blacked the user object, if it is blacked, the left side of the following expression is 1, otherwise it is 0'''
        return self.harassers.filter(
            blacklist.c.block_id == user.id).count() > 0

    def block(self, user):
        '''The current user started to block the user object user'''
        if not self.is_blocking(user):
            self.harassers.append(user)

    def unblock(self, user):
        '''The current user unblocks the user object'''
        if self.is_blocking(user):
            self.harassers.remove(user)

    def new_posts_likes(self):
        '''The new count of articles received by users that are liked'''
        last_read_time = self.last_posts_likes_read_time or datetime(1900, 1, 1)
        # Among the articles posted by current users, which articles are liked
        posts = self.posts.join(posts_likes).all()
        # New favorite record count
        new_likes_count = 0
        for p in posts:
            # Get like time
            for u in p.likers:
                if u != self:  # Users do not need to be notified if they like their articles
                    res = db.engine.execute("select * from posts_likes where user_id={} and post_id={}".format(u.id, p.id))
                    timestamp = datetime.strptime(str(list(res)[0][2]), '%Y-%m-%d %H:%M:%S.%f') #add str
                    # Determine whether this favorite record is new
                    if timestamp > last_read_time:
                        new_likes_count += 1
        return new_likes_count

    def new_properties_likes(self):
        '''The new count of articles received by users that are liked'''
        last_read_time = self.last_properties_likes_read_time or datetime(1900, 1, 1)
        #Among the articles posted by current users, which articles are liked
        properties = self.properties.join(properties_likes).all()
        # New favorite record count
        new_likes_count = 0
        for p in properties:
            # Get like time
            for u in p.likers:
                if u != self:  # Users do not need to be notified if they like their articles
                    res = db.engine.execute("select * from properties_likes where user_id={} and property_id={}".format(u.id, p.id))
                    timestamp = datetime.strptime(str(list(res)[0][2]), '%Y-%m-%d %H:%M:%S.%f')
                    #  Determine whether this favorite record is new
                    if timestamp > last_read_time:
                        new_likes_count += 1
        return new_likes_count

    def generate_confirm_jwt(self, expires_in=3600):
        '''Generate a JWT' to confirm the account'''
        now = datetime.utcnow()
        payload = {
            'confirm': self.id,
            'exp': now + timedelta(seconds=expires_in),
            'iat': now
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    def verify_confirm_jwt(self, token):
        '''After the user clicks the URL in the confirmation email, the JWT needs to be checked. If the check passes, the newly added confirmed attribute is set to True'''
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
        except (jwt.exceptions.ExpiredSignatureError,
                jwt.exceptions.InvalidSignatureError,
                jwt.exceptions.DecodeError) as e:
            # Token过期，或被人修改，那么签名验证也会失败
            return False
        if payload.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_password_jwt(self, expires_in=3600):
        '''Generate reset account password JWT'''
        now = datetime.utcnow()
        payload = {
            'reset_password': self.id,
            'exp': now + timedelta(seconds=expires_in),
            'iat': now
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_jwt(token):
        '''After the user clicks the URL in the password reset email, it needs to be checked JWT
        If the check is passed, return the user instance corresponding to the id stored in the JWT'''
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
        except (jwt.exceptions.ExpiredSignatureError,
                jwt.exceptions.InvalidSignatureError,
                jwt.exceptions.DecodeError) as e:
            # Token过期，或被人修改，那么签名验证也会失败
            return None
        return User.query.get(payload.get('reset_password'))

    def can(self, perm):
        '''检查用户是否有指定的权限'''
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        '''检查用户是否为管理员'''
        return self.can(Permission.ADMIN)

    def get_task_in_progress(self, name):
        '''检查指定任务名的RQ任务是否还在运行中'''
        return Task.query.filter_by(name=name, user=self, complete=False).first()

    def launch_task(self, name, description, *args, **kwargs):
        '''用户启动一个新的后台任务'''
        rq_job = current_app.task_queue.enqueue('app.utils.tasks.' + name, *args, **kwargs)
        task = Task(id=rq_job.get_id(), name=name, description=description, user=self)
        db.session.add(task)
        db.session.commit()
        return task

    def get_tasks_in_progress(self):
        '''返回用户所有正在运行中的后台任务'''
        return Task.query.filter_by(user=self, complete=False).all()

    def __repr__(self):
        return '<User {}>'.format(self.username)


class JsonEncodedDict(db.TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


mutable.MutableDict.associate_with(JsonEncodedDict)

class Post(SearchableMixin, PaginatedAPIMixin, db.Model):
    __tablename__ = 'posts'
    __searchable__ = [('title', True), ('summary', True), ('body', False)]
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    topic = db.Column(db.String(64))
    tags = db.Column(db.String(500))
    link_= db.Column(db.String(500))
    source = db.Column(db.String(500))
    audio_links = db.Column(db.PickleType)
    summary = db.Column(db.Text)
    image = db.Column(db.PickleType, nullable=True)#anhlbt
    body = db.Column(db.Text)
    json_book = db.Column(JsonEncodedDict)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    # Foreign keys, directly manipulate the database. When there are posts under the user, it is not allowed to delete the user. The following is just an ORM-level “delete” cascade
    # db.ForeignKey('users.id', ondelete='CASCADE') Will also specify the FOREIGN KEY level "ON DELETE" cascade in the database
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic',
                               cascade='all, delete-orphan')
    # A blog post has a many-to-many relationship with people who like/bookmark it
    likers = db.relationship('User', secondary=posts_likes, backref=db.backref('liked_posts', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Post {}>'.format(self.title)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        '''
        target: Post instance objects that listen for events
        value: Monitor which field changes
        '''
        if not target.summary:  # If the front end does not fill in the summary, it is empty str, not None
            target.summary = value[:200] + '  ... ...'  # Intercept the first 200 characters of the body field to summary

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'image':self.image,
            'body': self.body,
            'json_book':self.json_book,
            'timestamp': self.timestamp,
            'views': self.views,
            'likers_id': [user.id for user in self.likers],
            'likers': [
                {
                    'id': user.id,
                    'username': user.username,
                    'name': user.name,
                    'avatar': user.avatar(128)
                } for user in self.likers
            ],
            'author': {
                'id': self.author.id,
                'username': self.author.username,
                'name': self.author.name,
                'avatar': self.author.avatar(128)
            },
            'likers_count': self.likers.count(),
            'comments_count': self.comments.count(),
            '_links': {
                'self': url_for('api.get_post', id=self.id),
                'author_url': url_for('api.get_user', id=self.author_id),
                'comments': url_for('api.get_post_comments', id=self.id)
            },
            'source': self.source,
            'tags': self.tags,
            'topic': self.topic,
            'audio_links': self.audio_links
        }
        return data

    def from_dict(self, data):
        for field in ['title', 'summary', 'body', 'timestamp', 'views']:
            if field in data:
                setattr(self, field, data[field])

    def is_liked_by(self, user):
        '''Determine whether user user has bookmarked the articleer user has bookmarked the article'''
        return user in self.likers

    def liked_by(self, user):
        '''Favorites'''
        if not self.is_liked_by(user):
            self.likers.append(user)

    def unliked_by(self, user):
        '''Unfavorite'''
        if self.is_liked_by(user):
            self.likers.remove(user)


db.event.listen(Post.body, 'set', Post.on_changed_body)  # body 字段有变化时，执行 on_changed_body() 方法
db.event.listen(Post, 'after_insert', Post.receive_after_insert)
db.event.listen(Post, 'after_delete', Post.receive_after_delete)

class Property(SearchableMixin, PaginatedAPIMixin, db.Model):
    __tablename__ = 'properties'
    __searchable__ = [('title', True), ('address', True), ('nearby', False)]
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    slug = db.Column(db.String(200))
    price = db.Column(db.Float)
    promoted = db.Column(db.String(50))
    features = db.Column(postgresql.ARRAY(db.Text))
    purpose = db.Column(db.Enum(*['Sale', 'Rent', 'Other'], name='purpose'), default='Sale')
    type = db.Column(db.Enum(*['Apartment', 'Studio', 'House', 'Commercial', 'Land', 'Office', 'Other'], name='type'), default='House')
    # image = db.Column(db.String(200))
    images = db.Column(postgresql.ARRAY(db.String(500)))
    bedroom = db.Column(db.Integer)
    bathroom = db.Column(db.Integer)
    city = db.Column(db.String(200))
    city_slug = db.Column(db.String(200))
    address = db.Column(db.String(500))
    province =  db.Column(db.String(50))
    district =  db.Column(db.String(50))
    ward =  db.Column(db.String(50))
    area =  db.Column(db.String(200))
    total_area_sq_m =  db.Column(db.String(10))
    used_area_sq_m =  db.Column(db.String(10))
    direction = db.Column(db.String(50))
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.String(500))
    video = db.Column(db.String(200))
    floor_plan = db.Column(db.String(200))
    latitude = db.Column(db.String(50))
    longtitude = db.Column(db.String(50))
    nearby = db.Column(db.Text)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_at = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer)
    likers = db.relationship('User', secondary=properties_likes, backref=db.backref('liked_properties', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Property {}>'.format(self.title)

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            
            'slug' :self.slug,
            'price': self.price,
            'promoted' : self.promoted,
            'features' : self.features,
            'purpose' : self.purpose,
            'type' : self.type,
            # image = db.Column(db.String(200))
            'images' :self.images,
            'bedroom' :self.bedroom,
            'bathroom': self.bathroom,
            'city': self.city,
            'city_slug' :self.city_slug,
            'address': self.address,
            'province': self.province,
            'district': self.district,
            'ward': self.ward,
            'total_area_sq_m':self.total_area_sq_m,
            'used_area_sq_m': self.used_area_sq_m,
            'direction': self.direction,
            'area' :self.area,
            'agent_id' :self.agent_id,
            'description': self.description,
            'video' :self.video,
            'floor_plan' :self.floor_plan,
            'latitude' :self.latitude,
            'longtitude': self.longtitude,
            'nearby' :self.nearby,
            'created_at' :self.created_at,
            'updated_at' : self.updated_at,
            'post_at': self.post_at,
            'views': self.views,
            'likers_id': [user.id for user in self.likers],
            'likers': [
                {
                    'id': user.id,
                    'username': user.username,
                    'name': user.name,
                    'avatar': user.avatar(128)
                } for user in self.likers
            ],
            'author': {
                'id': self.author.id,
                'username': self.author.username,
                'name': self.author.name,
                'avatar': self.author.avatar(128)
            },
            'likers_count': self.likers.count(),
            # 'comments_count': self.comments.count(),
            '_links': {
                'self': url_for('api.get_property', id=self.id),
                'author_url': url_for('api.get_user', id=self.agent_id)
                # 'comments': url_for('api.get_property_comments', id=self.id)
                
            }
            
            # 'source': self.source,
            # 'tags': self.tags,
            # 'topic': self.topic,
            # 'audio_links': self.audio_links
        }
        return data


    def from_dict(self, data):
        for field in ['title', 'description', 'price','promoted', 'features', 'purpose', 'type','images',\
                       'bedroom', 'bathroom','city', 'address','province', 'district', 'ward', \
                        'total_area_sq_m', 'used_area_sq_m', 'direction', 'area', 'agent_id','video','floor_plan',\
                        'latitude','longtitude', 'nearby','created_at', 'updated_at', 'views', 'post_at']:     
            if field in data:
                setattr(self, field, data[field])
                # if field != 'post_at':
                #     setattr(self, field, data[field])
                # else:
                    # setattr(self, field, datetime.strptime(data[field], '%Y-%m-%d %H:%M:%S.%f'))
                    # setattr(self, field, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    # setattr(self, field, None)
    def is_liked_by(self, user):
        '''Determine whether user user has bookmarked the article'''
        return user in self.likers

    def liked_by(self, user):
        '''favorites'''
        if not self.is_liked_by(user):
            self.likers.append(user)

    def unliked_by(self, user):
        '''unfavorites'''
        if self.is_liked_by(user):
            self.likers.remove(user)


# db.event.listen(Property.title, 'set', Property.on_changed_body)  # body 字段有变化时，执行 on_changed_body() 方法
db.event.listen(Property, 'after_insert', Property.receive_after_insert)
db.event.listen(Property, 'after_delete', Property.receive_after_delete)                    
                     
                    
                        

class Comment(PaginatedAPIMixin, db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    mark_read = db.Column(db.Boolean, default=False)  # 文章作者会收到评论提醒，可以标为已读
    disabled = db.Column(db.Boolean, default=False)  # 屏蔽显示
    # 评论与对它点赞的人是多对多关系
    likers = db.relationship('User', secondary=comments_likes, backref=db.backref('liked_comments', lazy='dynamic'), lazy='dynamic')
    # 外键，评论作者的 id
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 外键，评论所属文章的 id
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    # 自引用的多级评论实现
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id', ondelete='CASCADE'))
    # 级联删除的 cascade 必须定义在 "多" 的那一侧，所以不能这样定义: parent = db.relationship('Comment', backref='children', remote_side=[id], cascade='all, delete-orphan')
    parent = db.relationship('Comment', backref=db.backref('children', cascade='all, delete-orphan'), remote_side=[id])

    def __repr__(self):
        return '<Comment {}>'.format(self.id)

    def get_descendants(self):
        '''获取评论的所有子孙'''
        data = set()

        def descendants(comment):
            if comment.children:
                data.update(comment.children)
                for child in comment.children:
                    descendants(child)
        descendants(self)
        return data

    def get_ancestors(self):
        '''Get all ancestors of comments'''
        data = []

        def ancestors(comment):
            if comment.parent:
                data.append(comment.parent)
                ancestors(comment.parent)
        ancestors(self)
        return data

    def to_dict(self):
        data = {
            'id': self.id,
            'body': self.body,
            'timestamp': self.timestamp,
            'mark_read': self.mark_read,
            'disabled': self.disabled,
            'likers_id': [user.id for user in self.likers],
            'author': {
                'id': self.author.id,
                'username': self.author.username,
                'name': self.author.name,
                'avatar': self.author.avatar(128)
            },
            'post': {
                'id': self.post.id,
                'title': self.post.title,
                'author_id': self.post.author.id
            },
            'parent_id': self.parent.id if self.parent else None,
            # 'children': [child.to_dict() for child in self.children] if self.children else None,
            '_links': {
                'self': url_for('api.get_comment', id=self.id),
                'author_url': url_for('api.get_user', id=self.author_id),
                'post_url': url_for('api.get_post', id=self.post_id),
                'parent_url': url_for('api.get_comment', id=self.parent.id) if self.parent else None,
                'children_url': [url_for('api.get_comment', id=child.id) for child in self.children] if self.children else None
            }
        }
        return data

    def from_dict(self, data):
        for field in ['body', 'timestamp', 'mark_read', 'disabled', 'author_id', 'post_id', 'parent_id']:
            if field in data:
                setattr(self, field, data[field])

    def is_liked_by(self, user):
        '''Determine whether user user has liked the comment'''
        return user in self.likers

    def liked_by(self, user):
        '''like'''
        if not self.is_liked_by(user):
            self.likers.append(user)

    def unliked_by(self, user):
        '''Unlike'''
        if self.is_liked_by(user):
            self.likers.remove(user)


class Notification(db.Model):  # No need for pagination
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def __repr__(self):
        return '<Notification {}>'.format(self.id)

    def get_data(self):
        return json.loads(str(self.payload_json))

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'name': self.user.name,
                'avatar': self.user.avatar(128)
            },
            'timestamp': self.timestamp,
            'payload': self.get_data(),
            '_links': {
                'self': url_for('api.get_notification', id=self.id),
                'user_url': url_for('api.get_user', id=self.user_id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['body', 'timestamp']:
            if field in data:
                setattr(self, field, data[field])


class Message(PaginatedAPIMixin, db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Message {}>'.format(self.id)

    def to_dict(self):
        data = {
            'id': self.id,
            'body': self.body,
            'timestamp': self.timestamp,
            'sender': self.sender.to_dict(),
            'recipient': self.recipient.to_dict(),
            '_links': {
                'self': url_for('api.get_message', id=self.id),
                'sender_url': url_for('api.get_user', id=self.sender_id),
                'recipient_url': url_for('api.get_user', id=self.recipient_id)
            }
        }
        return data

    def from_dict(self, data):
        for field in ['body', 'timestamp']:
            if field in data:
                setattr(self, field, data[field])


class Task(PaginatedAPIMixin, db.Model):
    __tablename__ = 'tasks'
    # 不使用默认的整数主键，而是用 RQ 为每个任务生成的字符串ID
    id = db.Column(db.String(36), primary_key=True)
    # 任务名
    name = db.Column(db.String(128), index=True)
    # 任务描述
    description = db.Column(db.String(128))
    # 任务所属的用户
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 是否已执行完成
    complete = db.Column(db.Boolean, default=False)

    def get_progress(self):
        '''返回Task对象实时的进度'''
        try:
            # 通过Task.id，返回RQ job实例
            rq_job = current_app.task_queue.fetch_job(self.id)
        except Exception:
            rq_job = None
        return rq_job.meta.get('progress', 0) if rq_job is not None else 100

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'progress': self.get_progress(),
            'complete': self.complete,
            '_links': {
                'user_url': url_for('api.get_user', id=self.user.id)
            }
        }
        return data

    def __repr__(self):
        return '<Task {}>'.format(self.id)
