from datetime import datetime
from operator import itemgetter
import re
from flask import request, jsonify, url_for, g, current_app
from flask_babel import gettext as _
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request, error_response
from app.extensions import db
from app.models import Permission, comments_likes, posts_likes, User, Post, Comment, Notification, Message, Task, Property
from app.utils.email import send_email
from app.utils.decorator import permission_required


@bp.route('/users/', methods=['POST'])
def create_user():
    '''Register a new user'''
    data = request.get_json()
    if not data:
        return bad_request(_('You must post JSON data.'))

    message = {}
    if 'username' not in data or not data.get('username', None).strip():
        message['username'] = _('Please provide a valid username.')
    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' not in data or not re.match(pattern, data.get('email', None)):
        message['email'] = _('Please provide a valid email address.')
    if 'password' not in data or not data.get('password', None).strip():
        message['password'] = _('Please provide a valid password.')

    if User.query.filter_by(username=data.get('username', None)).first():
        message['username'] = _('Please use a different username.')
    if User.query.filter_by(email=data.get('email', None)).first():
        message['email'] = _('Please use a different email address.')
    if message:
        return bad_request(message)

    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()

    # Send email confirming account
    token = user.generate_confirm_jwt()
    if not data.get('confirm_email_base_url'):
        confirm_url = 'http://127.0.0.1:5000/api/confirm/' + token
    else:
        confirm_url = data.get('confirm_email_base_url') + token

    text_body = '''
    Dear {},
    Welcome to Anhlbt's blog!
    To confirm your account please click on the following link: {}
    Sincerely,
    The Anhlbt's blog Team
    Note: replies to this email address are not monitored.
    '''.format(user.username, confirm_url)

    html_body = '''
    <p>Dear {0},</p>
    <p>Welcome to <b>Anhlbt's blog</b>!</p>
    <p>To confirm your account please <a href="{1}">click here</a>.</p>
    <p>Alternatively, you can paste the following link in your browser's address bar:</p>
    <p><b>{1}</b></p>
    <p>Sincerely,</p>
    <p>The Anhlbt's blog Team</p>
    <p><small>Note: replies to this email address are not monitored.</small></p>
    '''.format(user.username, confirm_url)

    send_email("[Anhlbt's blog] Confirm Your Account",
               sender=current_app.config['MAIL_SENDER'],
               recipients=[user.email],
               text_body=text_body,
               html_body=html_body)

    response = jsonify(user.to_dict())
    response.status_code = 201
    # The HTTP protocol requires the 201 response to contain a Location header whose value is the URL of the new resource
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/users/', methods=['GET'])
@token_auth.login_required
def get_users():
    '''Return user collection, pagination'''
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['USERS_PER_PAGE'], type=int), 100)
    data = User.to_collection_dict(User.query.order_by(User.member_since.desc()), page, per_page, 'api.get_users')
    return jsonify(data)


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    '''Return a user'''
    user = User.query.get_or_404(id)
    if g.current_user == user:
        return jsonify(user.to_dict(include_email=True))
    # If you are querying other users, add the flag bit whether you have followed this user
    data = user.to_dict()
    data['is_following'] = g.current_user.is_following(user)
    return jsonify(data)


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    '''Modify a user'''
    user = User.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return bad_request(_('You must post JSON data.'))

    message = {}
    if 'username' in data and not data.get('username', None).strip():
        message['username'] = _('Please provide a valid username.')

    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' in data and not re.match(pattern, data.get('email', None)):
        message['email'] = _('Please provide a valid email address.')

    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        message['username'] = _('Please use a different username.')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        message['email'] = _('Please use a different email address.')

    if message:
        return bad_request(message)

    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/users/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    '''Delete a user'''
    user = User.query.get_or_404(id)
    if g.current_user != user and not g.current_user.can(Permission.ADMIN):
        return error_response(403)
    db.session.delete(user)
    db.session.commit()
    return '', 204


@bp.route('/users/<int:id>/notifications/', methods=['GET'])
@token_auth.login_required
def get_user_notifications(id):
    '''Return new notifications for this user'''
    user = User.query.get_or_404(id)
    if g.current_user != user:
        return error_response(403)
    # Only return new notifications that have occurred since the last notification you saw
    # For example, a user requests the API once at 10:00:00, and requests the API again at 10:00:10 will only return new notifications generated after 10:00:00
    since = request.args.get('since', 0.0, type=float)
    notifications = user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([n.to_dict() for n in notifications])


###
# Follow / unfollow
###
@bp.route('/follow/<int:id>', methods=['GET'])
@token_auth.login_required
@permission_required(Permission.FOLLOW)
def follow(id):
    '''Start following a user'''
    user = User.query.get_or_404(id)
    if g.current_user == user:
        return bad_request(_('You cannot follow yourself.'))
    if g.current_user.is_following(user):
        return bad_request(_('You have already followed that user.'))
    g.current_user.follow(user)
    # Send this user a new fan notification
    user.add_notification('unread_follows_count', user.new_follows())
    db.session.commit()
    username = user.name if user.name else user.username
    return jsonify({
        'status': 'success',
        'message': _('You are now following %(username)s.', username=username)
    })


@bp.route('/unfollow/<int:id>', methods=['GET'])
@token_auth.login_required
@permission_required(Permission.FOLLOW)
def unfollow(id):
    '''Unfollow a user'''
    user = User.query.get_or_404(id)
    if g.current_user == user:
        return bad_request('You cannot unfollow yourself.')
    if not g.current_user.is_following(user):
        return bad_request('You are not following this user.')
    g.current_user.unfollow(user)
    # Send a new fan notification to the user (need to automatically subtract 1)
    user.add_notification('unread_follows_count', user.new_follows())
    db.session.commit()
    username = user.name if user.name else user.username
    return jsonify({
        'status': 'success',
        'message': _('You are not following %(username)s anymore.', username=username)
    })


###
#Who is the user following, and the user's fans
###
@bp.route('/users/<int:id>/followeds/', methods=['GET'])
@token_auth.login_required
def get_followeds(id):
    '''Return a list of people the user has followed'''
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['USERS_PER_PAGE'], type=int), 100)
    data = User.to_collection_dict(
        user.followeds, page, per_page, 'api.get_followeds', id=id)
    # Add the is_following flag to each followed
    for item in data['items']:
        item['is_following'] = g.current_user.is_following(
            User.query.get(item['id']))
        # Get the time when users started to follow followed
        res = db.engine.execute(
            "select * from followers where follower_id={} and followed_id={}".
            format(user.id, item['id']))
        item['timestamp'] = datetime.strptime(
            str(list(res)[0][2]), '%Y-%m-%d %H:%M:%S.%f')
    # Sort a list of dictionaries by timestamp (reverse order, with the most recent people at the top)
    data['items'] = sorted(data['items'], key=itemgetter('timestamp'), reverse=True)
    return jsonify(data)


@bp.route('/users/<int:id>/followers/', methods=['GET'])
@token_auth.login_required
def get_followers(id):
    '''Return the user's fan list'''
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['USERS_PER_PAGE'], type=int), 100)
    data = User.to_collection_dict(
        user.followers, page, per_page, 'api.get_followers', id=id)
    # Add the is_following flag for each follower
    for item in data['items']:
        item['is_following'] = g.current_user.is_following(
            User.query.get(item['id']))
        # Obtain the time when the follower started following the user
        res = db.engine.execute(
            "select * from followers where follower_id={} and followed_id={}".
            format(item['id'], user.id))
        item['timestamp'] = datetime.strptime(
            str(list(res)[0][2]), '%Y-%m-%d %H:%M:%S.%f')
    # Sort a list of dictionaries by timestamp (reverse order, with the latest fans at the top)
    data['items'] = sorted(data['items'], key=itemgetter('timestamp'), reverse=True)
    # Mark which fans are new
    last_read_time = user.last_follows_read_time or datetime(1900, 1, 1)
    for item in data['items']:
        if item['timestamp'] > last_read_time:
            item['is_new'] = True
    # Update the last_follows_read_time attribute value
    user.last_follows_read_time = datetime.utcnow()
    # Reset the count of new fan notifications
    user.add_notification('unread_follows_count', 0)
    db.session.commit()
    return jsonify(data)


###
# Resources related to user resources
##
@bp.route('/users/<int:id>/posts/', methods=['GET'])
@token_auth.login_required
def get_user_posts(id):
    '''Return a list of all blog posts of this user'''
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)
    data = Post.to_collection_dict(
        user.posts.order_by(Post.timestamp.desc()), page, per_page,
        'api.get_user_posts', id=id)
    return jsonify(data)


@bp.route('/users/<int:id>/properties/', methods=['GET'])
@token_auth.login_required
def get_user_properties(id):
    '''Return a list of all blog posts of this user'''
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)
    data = Property.to_collection_dict(
        user.properties.order_by(Property.created_at.desc()), page, per_page,
        'api.get_user_properties', id=id)
    return jsonify(data)

@bp.route('/users/<int:id>/liked-posts/', methods=['GET'])
@token_auth.login_required
def get_user_liked_posts(id):
    '''Return a list of articles that the user likes others'''
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)
    data = Post.to_collection_dict(
        user.liked_posts.order_by(Post.timestamp.desc()), page, per_page,
        'api.get_user_liked_posts', id=id)
    return jsonify(data)

@bp.route('/users/<int:id>/liked-properties/', methods=['GET'])
@token_auth.login_required
def get_user_liked_properties(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)
    data = Property.to_collection_dict(
        user.liked_properties.order_by(Property.created_at.desc()), page, per_page,
        'api.get_user_liked_properties', id=id)
    return jsonify(data)

@bp.route('/users/<int:id>/followeds-posts/', methods=['GET'])
@token_auth.login_required
def get_user_followeds_posts(id):
    '''Returns a list of all blog posts of the Great God that the user is following'''
    user = User.query.get_or_404(id)
    if g.current_user != user:
        return error_response(403)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)
    data = Post.to_collection_dict(
        user.followeds_posts().order_by(Post.timestamp.desc()), page, per_page,
        'api.get_user_followeds_posts', id=id)
    # Mark which articles are new
    last_read_time = user.last_followeds_posts_read_time or datetime(1900, 1, 1)
    for item in data['items']:
        if item['timestamp'] > last_read_time:
            item['is_new'] = True
    # Update the last_followeds_posts_read_time attribute value
    user.last_followeds_posts_read_time = datetime.utcnow()
    # Reset the count of new article notifications
    user.add_notification('unread_followeds_posts_count', 0)
    db.session.commit()
    return jsonify(data)



@bp.route('/users/<int:id>/comments/', methods=['GET'])
@token_auth.login_required
def get_user_comments(id):
    '''Returns a list of all comments posted by this user'''
    user = User.query.get_or_404(id)
    if g.current_user != user:
        return error_response(403)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['COMMENTS_PER_PAGE'], type=int), 100)
    data = Comment.to_collection_dict(
        user.comments.order_by(Comment.timestamp.desc()), page, per_page,
        'api.get_user_comments', id=id)
    return jsonify(data)


@bp.route('/users/<int:id>/recived-comments/', methods=['GET'])
@token_auth.login_required
def get_user_recived_comments(id):
    '''Return all comments received by this user'''
    user = User.query.get_or_404(id)
    if g.current_user != user:
        return error_response(403)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['COMMENTS_PER_PAGE'], type=int), 100)
    # A collection of all article IDs published by the user
    user_posts_ids = [post.id for post in user.posts.all()]
    #The new comment below the user’s post, that is, the post_id of the comment is in the user_posts_ids collection, and the author of the comment is not himself (the author of the post)
    q1 = Comment.query.filter(Comment.post_id.in_(user_posts_ids), Comment.author != user)
    # User comments were replied
    descendants = set()
    for c in user.comments:
        descendants = descendants | c.get_descendants()
    descendants = descendants - set(user.comments.all())  # Get rid of the reply from the bottom
    descendants_ids = [c.id for c in descendants]
    q2 = Comment.query.filter(Comment.id.in_(descendants_ids))
    # Arrange in reverse chronological order to form all the comments received by the user
    recived_comments = q1.union(q2).order_by(Comment.mark_read, Comment.timestamp.desc())
    # JSON data after pagination
    data = Comment.to_collection_dict(recived_comments, page, per_page, 'api.get_user_recived_comments', id=id)
    # Mark which comments are new
    last_read_time = user.last_recived_comments_read_time or datetime(1900, 1, 1)
    for item in data['items']:
        if item['timestamp'] > last_read_time:
            item['is_new'] = True
    # Update the last_recived_comments_read_time attribute value
    user.last_recived_comments_read_time = datetime.utcnow()
    # Reset the count of new comment notifications
    user.add_notification('unread_recived_comments_count', 0)
    db.session.commit()
    return jsonify(data)


@bp.route('/users/<int:id>/recived-comments-likes/', methods=['GET'])
@token_auth.login_required
def get_user_recived_comments_likes(id):
    '''Return comment likes received by this user'''
    user = User.query.get_or_404(id)
    if g.current_user != user:
        return error_response(403)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['COMMENTS_PER_PAGE'], type=int), 100)
    # Which user comments are liked, pagination
    comments = user.comments.join(comments_likes).paginate(page, per_page)
    # Like record
    records = {
        'items': [],
        '_meta': {
            'page': page,
            'per_page': per_page,
            'total_pages': comments.pages,
            'total_items': comments.total
        },
        '_links': {
            'self': url_for('api.get_user_recived_comments_likes', page=page, per_page=per_page, id=id),
            'next': url_for('api.get_user_recived_comments_likes', page=page + 1, per_page=per_page, id=id) if comments.has_next else None,
            'prev': url_for('api.get_user_recived_comments_likes', page=page - 1, per_page=per_page, id=id) if comments.has_prev else None
        }
    }
    for c in comments.items:
        # Reorganize the data to become: (who) (when) liked you (which comment)
        for u in c.likers:
            if u != user:  # Users who like their own comments do not need to be notified
                data = {}
                data['user'] = u.to_dict()
                data['comment'] = c.to_dict()
                # Time to get likes
                res = db.engine.execute("select * from comments_likes where user_id={} and comment_id={}".format(u.id, c.id))
                data['timestamp'] = datetime.strptime(str(list(res)[0][2]), '%Y-%m-%d %H:%M:%S.%f')
                # Mark whether this like record is new
                last_read_time = user.last_comments_likes_read_time or datetime(1900, 1, 1)
                if data['timestamp'] > last_read_time:
                    data['is_new'] = True
                records['items'].append(data)
    # Sort a list of dictionaries by timestamp (reverse order, with the most recent likes at the top)
    records['items'] = sorted(records['items'], key=itemgetter('timestamp'), reverse=True)
    # Update the last_comments_likes_read_time attribute value
    user.last_comments_likes_read_time = datetime.utcnow()
    # Reset the count of new like notifications to zero
    user.add_notification('unread_comments_likes_count', 0)
    db.session.commit()
    return jsonify(records)


@bp.route('/users/<int:id>/recived-posts-likes/', methods=['GET'])
@token_auth.login_required
def get_user_recived_posts_likes(id):
    '''Return article likes received by this user'''
    user = User.query.get_or_404(id)
    if g.current_user != user:
        return error_response(403)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)
    # Which articles have been liked/favored by users, pagination
    posts = user.posts.join(posts_likes).paginate(page, per_page)
    # Like to record
    records = {
        'items': [],
        '_meta': {
            'page': page,
            'per_page': per_page,
            'total_pages': posts.pages,
            'total_items': posts.total
        },
        '_links': {
            'self': url_for('api.get_user_recived_posts_likes', page=page, per_page=per_page, id=id),
            'next': url_for('api.get_user_recived_posts_likes', page=page + 1, per_page=per_page, id=id) if posts.has_next else None,
            'prev': url_for('api.get_user_recived_posts_likes', page=page - 1, per_page=per_page, id=id) if posts.has_prev else None
        }
    }
    for p in posts.items:
        # Reorganize the data to become: (who) (when) liked yours (which article)
        for u in p.likers:
            if u != user:  # Users do not need to be notified if they like their articles
                data = {}
                data['user'] = u.to_dict()
                data['post'] = p.to_dict()
                # Get like time
                res = db.engine.execute("select * from posts_likes where user_id={} and post_id={}".format(u.id, p.id))
                data['timestamp'] = datetime.strptime(str(list(res)[0][2]), '%Y-%m-%d %H:%M:%S.%f')
                # Mark whether this favorite record is new
                last_read_time = user.last_posts_likes_read_time or datetime(1900, 1, 1)
                if data['timestamp'] > last_read_time:
                    data['is_new'] = True
                records['items'].append(data)
    # Sort a list of dictionaries by timestamp (reverse order, with the most recent favorite at the top)
    records['items'] = sorted(records['items'], key=itemgetter('timestamp'), reverse=True)
    # Update the last_posts_likes_read_time attribute value
    user.last_posts_likes_read_time = datetime.utcnow()
    # Reset the count of new like notifications to zero
    user.add_notification('unread_posts_likes_count', 0)
    db.session.commit()
    return jsonify(records)


@bp.route('/users/<int:id>/messages-recipients/', methods=['GET'])
@token_auth.login_required
def get_user_messages_recipients(id):
    '''Which users have I sent private messages, group by users, and return the last private message I sent to each user
    That is: I sent (what private message) to (who) the last time'''
    user = User.query.get_or_404(id)
    if g.current_user != user:
        return error_response(403)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['MESSAGES_PER_PAGE'], type=int), 100)
    data = Message.to_collection_dict(
        user.messages_sent.group_by(Message.recipient_id).order_by(Message.timestamp.desc()), page, per_page,
        'api.get_user_messages_recipients', id=id)
    # I send a private message to each user, do they have unread
    for item in data['items']:
        # To whom
        recipient = User.query.get(item['recipient']['id'])
        # How many have been sent to him in total
        item['total_count'] = user.messages_sent.filter_by(recipient_id=item['recipient']['id']).count()
        #The last time he checked the received private message
        last_read_time = recipient.last_messages_read_time or datetime(1900, 1, 1)
        # item is the last one sent to him, if the last one is not new, there will be none
        if item['timestamp'] > last_read_time:
            item['is_new'] = True
            # Continue to get the private messages sent to this user, a few of which are new
            item['new_count'] = user.messages_sent.filter_by(recipient_id=item['recipient']['id']).filter(Message.timestamp > last_read_time).count()
    return jsonify(data)


@bp.route('/users/<int:id>/messages-senders/', methods=['GET'])
@token_auth.login_required
def get_user_messages_senders(id):
    '''Which users have sent me private messages, group by users, and return the last private message sent by each user
    That is: (who) sent me the last time (what private message)'''
    user = User.query.get_or_404(id)
    if g.current_user != user:
        return error_response(403)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['MESSAGES_PER_PAGE'], type=int), 100)
    data = Message.to_collection_dict(
        user.messages_received.group_by(Message.sender_id, Message.id).order_by(Message.timestamp.desc()), page, per_page,
        'api.get_user_messages_senders', id=id)
    # Is there any new private message sent to me by this user?
    last_read_time = user.last_messages_read_time or datetime(1900, 1, 1)
    new_items = []  # The last one is new
    not_new_items = []  # The last one is not new
    for item in data['items']:
        # Judge if I blocked him
        if user.is_blocking(User.query.get(item['sender']['id'])):
            item['is_blocking'] = True
        # item is the last one he sent, if the last one is not new, there is definitely no
        if item['timestamp'] > last_read_time:
            item['is_new'] = True
            # Continue to get the private messages sent by this user, a few of which are new
            item['new_count'] = user.messages_received.filter_by(sender_id=item['sender']['id']).filter(Message.timestamp > last_read_time).count()
            new_items.append(item)
        else:
            not_new_items.append(item)
    #The last one is new and sorted by timestamp in positive order, otherwise the user updating last_messages_read_time will cause all the ones with the first time to be marked as read
    new_items = sorted(new_items, key=itemgetter('timestamp'))
    data['items'] = new_items + not_new_items
    return jsonify(data)


@bp.route('/users/<int:id>/history-messages/', methods=['GET'])
@token_auth.login_required
def get_user_history_messages(id):
    '''Return all private message records between me and a user (obtained by the query parameter from)'''
    user = User.query.get_or_404(id)
    if g.current_user != user:
        return error_response(403)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['MESSAGES_PER_PAGE'], type=int), 100)
    from_id = request.args.get('from', type=int)
    if not from_id:  # Must provide the ID of the chatting user
        return bad_request('You must provide the user id of opposite site.')
    # Sent to me
    q1 = Message.query.filter(Message.sender_id == from_id, Message.recipient_id == id)
    # I sent to each other
    q2 = Message.query.filter(Message.sender_id == id, Message.recipient_id == from_id)
    # Arrange in positive time order to form a complete dialogue timeline
    history_messages = q1.union(q2).order_by(Message.timestamp)
    data = Message.to_collection_dict(history_messages, page, per_page, 'api.get_user_history_messages', id=id)
    # The data['items'] on this page now contains what the other party sent to me and me
    # Need to create a new list, only include the other party sent to me, to see which private messages are new
    recived_messages = [item for item in data['items'] if item['sender']['id'] != id]
    sent_messages = [item for item in data['items'] if item['sender']['id'] == id]
    # 然后，标记哪些私信是新的
    last_read_time = user.last_messages_read_time or datetime(1900, 1, 1)
    new_count = 0
    for item in recived_messages:
        if item['timestamp'] >= last_read_time:
            item['is_new'] = True
            new_count += 1
    if new_count > 0:
        # Update the last_messages_read_time attribute value to the last (recent) time of the received private message list
        user.last_messages_read_time = recived_messages[-1]['timestamp']
        db.session.commit()  # Submit the database first so that user.new_recived_messages() will change
        # Update the user's new private message notification count
        user.add_notification('unread_messages_count', user.new_recived_messages())
        db.session.commit()
    # Finally, regroup data['items'], because the new private message received is added with the is_new tag
    messages = recived_messages + sent_messages
    messages.sort(key=data['items'].index)  # 保持 messages 列表元素的顺序跟 data['items'] 一样
    data['items'] = messages
    return jsonify(data)


@bp.route('/users/<int:id>/tasks/', methods=['GET'])
@token_auth.login_required
def get_user_tasks_in_progress(id):
    '''Return all running background tasks of the user'''
    user = User.query.get_or_404(id)
    if g.current_user != user:
        return error_response(403)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['TASKS_PER_PAGE'], type=int), 100)
    data = Task.to_collection_dict(
        Task.query.filter_by(user=user, complete=False), page, per_page,
        'api.get_user_tasks_in_progress', id=id)
    return jsonify(data)


###
# 拉黑 / 取消拉黑
###
@bp.route('/block/<int:id>', methods=['GET'])
@token_auth.login_required
@permission_required(Permission.FOLLOW)
def block(id):
    '''Start to block a user'''
    user = User.query.get_or_404(id)
    if g.current_user == user:
        return bad_request('You cannot block yourself.')
    if g.current_user.is_blocking(user):
        return bad_request('You have already blocked that user.')
    g.current_user.block(user)
    db.session.commit()
    username = user.name if user.name else user.username
    return jsonify({
        'status': 'success',
        'message': _('You are now blocking %(username)s.', username=username)
    })


@bp.route('/unblock/<int:id>', methods=['GET'])
@token_auth.login_required
@permission_required(Permission.FOLLOW)
def unblock(id):
    '''Unblock a user'''
    user = User.query.get_or_404(id)
    if g.current_user == user:
        return bad_request('You cannot unblock yourself.')
    if not g.current_user.is_blocking(user):
        return bad_request('You are not blocking this user.')
    g.current_user.unblock(user)
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': _('You are not blocking %(username)s anymore.', username=username)
    })


@bp.route('/resend-confirm', methods=['POST'])
@token_auth.login_required
def resend_confirmation():
    '''Resend the email confirming the account'''
    data = request.get_json()
    if not data:
        return bad_request(_('You must post JSON data.'))
    if 'confirm_email_base_url' not in data or not data.get('confirm_email_base_url').strip():
        return bad_request(_('Please provide a valid confirm email base url.'))

    token = g.current_user.generate_confirm_jwt()

    text_body = '''
    Dear {},
    Welcome to Anhlbt's blog!
    To confirm your account please click on the following link: {}
    Sincerely,
    The Anhlbt's blog Team
    Note: replies to this email address are not monitored.
    '''.format(g.current_user.username, data.get('confirm_email_base_url') + token)

    html_body = '''
    <p>Dear {0},</p>
    <p>Welcome to <b>Anhlbt's blog</b>!</p>
    <p>To confirm your account please <a href="{1}">click here</a>.</p>
    <p>Alternatively, you can paste the following link in your browser's address bar:</p>
    <p><b>{1}</b></p>
    <p>Sincerely,</p>
    <p>The Anhlbt's blog Team</p>
    <p><small>Note: replies to this email address are not monitored.</small></p>
    '''.format(g.current_user.username, data.get('confirm_email_base_url') + token)

    send_email("[Anhlbt's blog] Confirm Your Account",
               sender=current_app.config['MAIL_SENDER'],
               recipients=[g.current_user.email],
               text_body=text_body,
               html_body=html_body)
    return jsonify({
        'status': 'success',
        'message': _('A new confirmation email has been sent to you by email.')
    })


@bp.route('/confirm/<token>', methods=['GET'])
@token_auth.login_required
def confirm(token):
    '''After the user receives the verification email, verify their account'''
    if g.current_user.confirmed:
        return bad_request(_('You have already confirmed your account.'))
    if g.current_user.verify_confirm_jwt(token):
        g.current_user.ping()
        db.session.commit()
        # 给用户发放新 JWT，因为要包含 confirmed: true
        token = g.current_user.get_jwt()
        return jsonify({
            'status': 'success',
            'message': _('You have confirmed your account. Thanks!'),
            'token': token
        })
    else:
        return bad_request(_('The confirmation link is invalid or has expired.'))


@bp.route('/reset-password-request', methods=['POST'])
def reset_password_request():
    '''Request to reset the account password, you need to provide the email address filled in during registration'''
    data = request.get_json()
    if not data:
        return bad_request(_('You must post JSON data.'))

    message = {}
    if 'confirm_email_base_url' not in data or not data.get('confirm_email_base_url').strip():
        message['confirm_email_base_url'] = _('Please provide a valid confirm email base url.')
    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' not in data or not re.match(pattern, data.get('email', None)):
        message['email'] = _('Please provide a valid email address.')
    if message:
        return bad_request(message)

    user = User.query.filter_by(email=data.get('email')).first()
    if user:  # If the user instance object corresponding to the provided email address exists, send an email
        token = user.generate_reset_password_jwt()

        text_body = '''
        Dear {0},
        To reset your password click on the following link: {1}
        If you have not requested a password reset simply ignore this message.
        Sincerely,
        The Anhlbt's blog Team
        Note: replies to this email address are not monitored.
        '''.format(user.username, data.get('confirm_email_base_url') + token)

        html_body = '''
        <p>Dear {0},</p>
        <p>To reset your password <a href="{1}">click here</a>.</p>
        <p>Alternatively, you can paste the following link in your browser's address bar:</p>
        <p><b>{1}</b></p>
        <p>If you have not requested a password reset simply ignore this message.</p>
        <p>Sincerely,</p>
        <p>The Anhlbt's blog Team</p>
        <p><small>Note: replies to this email address are not monitored.</small></p>
        '''.format(user.username, data.get('confirm_email_base_url') + token)

        send_email("[Anhlbt's blog] Reset Your Password",
                   sender=current_app.config['MAIL_SENDER'],
                   recipients=[user.email],
                   text_body=text_body,
                   html_body=html_body)
    # Regardless of whether the email address provided by the front end has a corresponding user instance (does not rule out someone who wants to maliciously reset someone else's account), respond to him
    return jsonify({
        'status': 'success',
        'message': _('An email with instructions to reset your password has been sent to you.')
    })


@bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    '''The user clicks on the link in the email to reset the password of the corresponding account by verifying the JWT'''
    data = request.get_json()
    if not data:
        return bad_request(_('You must post JSON data.'))
    if 'password' not in data or not data.get('password', None).strip():
        return bad_request(_('Please provide a valid password.'))
    user = User.verify_reset_password_jwt(token)
    if not user:
        return bad_request(_('The reset password link is invalid or has expired.'))
    user.set_password(data.get('password'))
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': _('Your password has been reset.')
    })


@bp.route('/update-password', methods=['POST'])
@token_auth.login_required
def update_password():
    '''The logged-in user updates his password'''
    data = request.get_json()
    if not data:
        return bad_request(_('You must post JSON data.'))

    if 'old_password' not in data or not data.get('old_password', None).strip():
        return bad_request(_('Please provide a valid old password.'))
    if 'new_password' not in data or not data.get('new_password', None).strip():
        return bad_request(_('Please provide a valid new password.'))
    if data.get('old_password') == data.get('new_password'):
        return bad_request(_('The new password is equal to the old password.'))
    # 验证旧密码
    if not g.current_user.check_password(data.get('old_password')):
        return bad_request(_('The old password is wrong.'))
    g.current_user.set_password(data.get('new_password'))
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': _('Your password has been updated.')
    })
