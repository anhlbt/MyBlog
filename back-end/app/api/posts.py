from flask import request, jsonify, url_for, g, current_app
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response, bad_request
from app.extensions import db
from app.models import Permission, Post, Comment
from app.utils.decorator import permission_required
import pdb

@bp.route('/posts/', methods=['POST'])
@token_auth.login_required
@permission_required(Permission.WRITE)
def create_post():
    '''Add a new article'''
    # pdb.set_trace()
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    message = {}
    if 'title' not in data or not data.get('title').strip():
        message['title'] = 'Title is required.'
    elif len(data.get('title')) > 255:
        message['title'] = 'Title must less than 255 characters.'
    if 'body' not in data or not data.get('body').strip():
        message['body'] = 'Body is required.'
    if message:
        return bad_request(message)

    post = Post()
    post.from_dict(data)
    post.author = g.current_user  # Passed by verify_token() in auth.py (in the same request, Token authentication is required)
    db.session.add(post)
    # Send a new article notification to all fans of the article author
    for user in post.author.followers:
        user.add_notification('unread_followeds_posts_count',
                              user.new_followeds_posts())
    db.session.commit()
    response = jsonify(post.to_dict())
    response.status_code = 201
    # The HTTP protocol requires the 201 response to contain a Location header whose value is the URL of the new resource
    response.headers['Location'] = url_for('api.get_post', id=post.id)
    return response


@bp.route('/posts/', methods=['GET'])
def get_posts():
    '''Return to the collection of articles, pagination'''
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)
    data = Post.to_collection_dict(
        Post.query.order_by(Post.timestamp.desc()), page, per_page, 'api.get_posts')
    return jsonify(data)

#get posts by topic
@bp.route('/posts/<topic>', methods=['GET'])
def get_post_by_topic(topic):
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)
    data = Post.to_collection_dict(Post.query.filter(Post.topic == topic), page, per_page, 'api.get_post_by_topic', topic=topic)
    return jsonify(data)


# #get posts by except topic
# @bp.route('/posts/<topic>', methods=['GET'])
# def get_post_except_topic(topic):
#     page = request.args.get('page', 1, type=int)
#     per_page = min(
#         request.args.get(
#             'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 10)
#     data = Post.to_collection_dict(Post.query.filter(Post.topic != topic), page, per_page, 'api.get_post_except_topic', topic=topic)
#     return jsonify(data)


@bp.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    '''Return to an article'''
    post = Post.query.get_or_404(id)
    post.views += 1
    db.session.add(post)
    db.session.commit()
    data = post.to_dict()
    # Next article
    next_basequery = Post.query.order_by(Post.timestamp.desc()).filter(Post.timestamp > post.timestamp)
    if next_basequery.all():
        data['next_id'] = next_basequery[-1].id
        data['next_title'] = next_basequery[-1].title
        data['_links']['next'] = url_for('api.get_post', id=next_basequery[-1].id)
    else:
        data['_links']['next'] = None
    # Previous article
    prev_basequery = Post.query.order_by(Post.timestamp.desc()).filter(Post.timestamp < post.timestamp)
    if prev_basequery.first():
        data['prev_id'] = prev_basequery.first().id
        data['prev_title'] = prev_basequery.first().title
        data['_links']['prev'] = url_for('api.get_post', id=prev_basequery.first().id)
    else:
        data['_links']['prev'] = None
    return jsonify(data)


@bp.route('/posts/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_post(id):
    '''Edit an article'''
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and not g.current_user.can(Permission.ADMIN):
        return error_response(403)

    data = request.get_json()
    print(data)
    # pdb.set_trace()
    if not data:
        return bad_request('You must post JSON data.')
    message = {}
    if 'title' not in data or not data.get('title').strip():
        message['title'] = 'Title is required.'
    elif len(data.get('title')) > 255:
        message['title'] = 'Title must less than 255 characters.'
    if 'body' not in data or not data.get('body').strip():
        message['body'] = 'Body is required.'
    if message:
        return bad_request(message)

    post.from_dict(data)
    db.session.commit()
    return jsonify(post.to_dict())


@bp.route('/posts/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_post(id):
    '''Delete an article'''
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and not g.current_user.can(Permission.ADMIN):
        return error_response(403)
    db.session.delete(post)
    # 给文章作者的所有粉丝发送新文章通知(需要自动减1)
    for user in post.author.followers:
        user.add_notification('unread_followeds_posts_count',
                              user.new_followeds_posts())
    db.session.commit()
    return '', 204


###
# Resources related to blog post resources
##
@bp.route('/posts/<int:id>/comments/', methods=['GET'])
def get_post_comments(id):
    '''Return to the first level comment below the current article'''
    post = Post.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['COMMENTS_PER_PAGE'], type=int), 100)
    # Get first level comments first
    data = Comment.to_collection_dict(
        post.comments.filter(Comment.parent==None).order_by(Comment.timestamp.desc()), page, per_page,
        'api.get_post_comments', id=id)
    # Then add descendants to the descendants attribute of the first-level comment
    for item in data['items']:
        comment = Comment.query.get(item['id'])
        descendants = [child.to_dict() for child in comment.get_descendants()]
        # 按 timestamp 排序一个字典列表
        from operator import itemgetter
        item['descendants'] = sorted(descendants, key=itemgetter('timestamp'))
    return jsonify(data)


###
# Article was liked/favored or unfavored/unfavored
###
@bp.route('/posts/<int:id>/like', methods=['GET'])
@token_auth.login_required
def like_post(id):
    '''Like article'''
    post = Post.query.get_or_404(id)
    post.liked_by(g.current_user)
    db.session.add(post)
    # Remember to submit first, first add the like record to the database, because new_posts_likes() will query the posts_likes association table    
    db.session.commit()
    # Send new like notifications to article authors
    post.author.add_notification('unread_posts_likes_count', post.author.new_posts_likes())
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': 'You are now liking this post.'
    })


@bp.route('/posts/<int:id>/unlike', methods=['GET'])
@token_auth.login_required
def unlike_post(id):
    '''Unlike article'''
    post = Post.query.get_or_404(id)
    post.unliked_by(g.current_user)
    db.session.add(post)
    # Remember to submit first and add the likes record to the database first, because new_posts_likes() will query the posts_likes association table
    db.session.commit()
    # Send a new like notification to the author of the article (need to automatically subtract 1)
    post.author.add_notification('unread_posts_likes_count',
                                 post.author.new_posts_likes())
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': 'You are not liking this post anymore.'
    })


@bp.route('/posts/export-posts/', methods=['GET'])
@token_auth.login_required
@permission_required(Permission.WRITE)
def export_posts():
    '''导出当前用户的所有文章，RQ 后台任务'''
    if g.current_user.get_task_in_progress('export_posts'):  # 如果用户已经有同名的后台任务在运行中时
        return bad_request('The background task of the last exported article has not ended')
    else:
        # 将 app.utils.tasks.export_posts 放入任务队列中
        g.current_user.launch_task('export_posts', 'Exporting articles...', kwargs={'user_id': g.current_user.id})
        return jsonify(message='Background task for exporting articles is running')


###
# 全文搜索
###
@bp.route('/search/', methods=['GET'])
def search():
    '''Elasticsearch全文检索博客文章'''
    q = request.args.get('q')
    if not q:
        return bad_request(message='keyword is required.')

    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)

    total, hits_basequery = Post.search(q, page, per_page)
    # 总页数
    total_pages, div = divmod(total, per_page)
    if div > 0:
        total_pages += 1

    # 不能使用 Post.to_collection_dict()，因为查询结果已经分页过了
    data = {
        'items': [item.to_dict() for item in hits_basequery],
        '_meta': {
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_items': total
        },
        '_links': {
            'self': url_for('api.search', q=q, page=page, per_page=per_page),
            'next': url_for('api.search', q=q, page=page + 1, per_page=per_page) if page < total_pages else None,
            'prev': url_for('api.search', q=q, page=page - 1, per_page=per_page) if page > 1 else None
        }
    }
    return jsonify(data=data, message='Total items: {}, current page: {}'.format(total, page))


@bp.route('/search/post-detail/<int:id>', methods=['GET'])
def get_search_post(id):
    '''Jump to article details from the search result list page'''
    q = request.args.get('q')
    page = request.args.get('page', type=int)
    per_page = request.args.get('per_page', type=int)

    if q and page and per_page:  # The description is from the search results page to view the details of the article, so highlight the keywords
        total, hits_basequery = Post.search(q, page, per_page)
        post = hits_basequery.first()  # There will be only one article
        data = post.to_dict()  # Will highlight keywords
    else:
        post = Post.query.get_or_404(id)
        data = post.to_dict()  # Will not highlight keywords

    # Next article
    next_basequery = Post.query.order_by(Post.timestamp.desc()).filter(Post.timestamp > post.timestamp)
    if next_basequery.all():
        data['next_id'] = next_basequery[-1].id
        data['next_title'] = next_basequery[-1].title
        data['_links']['next'] = url_for('api.get_post', id=next_basequery[-1].id)
    else:
        data['_links']['next'] = None
    # Previous article
    prev_basequery = Post.query.order_by(Post.timestamp.desc()).filter(Post.timestamp < post.timestamp)
    if prev_basequery.first():
        data['prev_id'] = prev_basequery.first().id
        data['prev_title'] = prev_basequery.first().title
        data['_links']['prev'] = url_for('api.get_post', id=prev_basequery.first().id)
    else:
        data['_links']['prev'] = None
    return jsonify(data)
