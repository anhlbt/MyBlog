from flask import request, jsonify, url_for, g, current_app
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response, bad_request
from app.extensions import db
from app.models import Permission, Post, Comment
from app.utils.decorator import permission_required


@bp.route('/comments/', methods=['POST'])
@token_auth.login_required
@permission_required(Permission.COMMENT)
def create_comment():
    '''Post a new comment below a blog post'''
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    if 'body' not in data or not data.get('body').strip():
        return bad_request('Body is required.')
    if 'post_id' not in data or not data.get('post_id'):
        return bad_request('Post id is required.')

    post = Post.query.get_or_404(int(data.get('post_id')))
    comment = Comment()
    comment.from_dict(data)
    comment.author = g.current_user
    comment.post = post
    # The comment must be added first, and User.new_recived_comments() can be the updated value when a notification is sent to each user later
    db.session.add(comment)
    db.session.commit()  #Update the database, add comment records
    # When adding a comment:
    # 1.If it is a first-level comment, just send a new comment notification to the author of the article
    # 2. If it is not a first-level comment, you need to send a new comment notification to the author of the article and the authors of all ancestors of the comment
    users = set()
    users.add(comment.post.author)  # Add the author of the article to the collection
    if comment.parent:
        ancestors_authors = {c.author for c in comment.get_ancestors()}
        users = users | ancestors_authors
    # Send a new comment notification to each user
    for u in users:
        u.add_notification('unread_recived_comments_count',
                           u.new_recived_comments())
    db.session.commit()  # Update database, write new notification
    response = jsonify(comment.to_dict())
    response.status_code = 201
    # The HTTP protocol requires the 201 response to contain a Location header whose value is the URL of the new resource
    response.headers['Location'] = url_for('api.get_comment', id=comment.id)
    return response


@bp.route('/comments/', methods=['GET'])
@token_auth.login_required
def get_comments():
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['COMMENTS_PER_PAGE'], type=int), 100)
    data = Comment.to_collection_dict(
        Comment.query.order_by(Comment.timestamp.desc()), page, per_page,
        'api.get_comments')
    return jsonify(data)


@bp.route('/comments/<int:id>', methods=['GET'])
@token_auth.login_required
def get_comment(id):
    '''Return a single comment'''
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_dict())


@bp.route('/comments/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_comment(id):
    '''Edit a single comment'''
    comment = Comment.query.get_or_404(id)
    if g.current_user != comment.author and g.current_user != comment.post.author and not g.current_user.can(Permission.ADMIN):
        return error_response(403)
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    # if 'body' not in data or not data.get('body'):
    #     return bad_request('Body is required.')
    comment.from_dict(data)
    db.session.commit()
    return jsonify(comment.to_dict())


@bp.route('/comments/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_comment(id):
    '''Delete a single comment'''
    comment = Comment.query.get_or_404(id)
    if g.current_user != comment.author and g.current_user != comment.post.author and not g.current_user.can(Permission.ADMIN):
        return error_response(403)
    # When deleting a comment:
    # 1. If it is a first-level comment, just send a new comment notification to the author of the article
    # 2. If it is not a first-level comment, you need to send a new comment notification to the author of the article and the authors of all ancestors of the comment
    users = set()
    users.add(comment.post.author)  # Add the author of the article to the collection
    if comment.parent:
        ancestors_authors = {c.author for c in comment.get_ancestors()}
        users = users | ancestors_authors
    # The comment must be deleted first, and User.new_recived_comments() can be the updated value when sending notifications to each user later
    db.session.delete(comment)
    db.session.commit()  # Update database, delete comment records
    # Send a new comment notification to each user
    for u in users:
        u.add_notification('unread_recived_comments_count',
                           u.new_recived_comments())
    db.session.commit()  # Update database, write new notification
    return '', 204


###
# Comments are liked or disliked
###
@bp.route('/comments/<int:id>/like', methods=['GET'])
@token_auth.login_required
@permission_required(Permission.COMMENT)
def like_comment(id):
    '''Like comment'''
    comment = Comment.query.get_or_404(id)
    comment.liked_by(g.current_user)
    db.session.add(comment)
    # Remember to submit first, and add the likes to the database first, because new_comments_likes() will query the comments_likes association table
    db.session.commit()
    # Send a new like notification to the comment author
    comment.author.add_notification('unread_comments_likes_count', comment.author.new_comments_likes())
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': 'You are now liking this comment.'
    })


@bp.route('/comments/<int:id>/unlike', methods=['GET'])
@token_auth.login_required
@permission_required(Permission.COMMENT)
def unlike_comment(id):
    '''Cancel like comment'''
    comment = Comment.query.get_or_404(id)
    comment.unliked_by(g.current_user)
    db.session.add(comment)
# Remember to submit first, first add the like record to the database, because new_comments_likes() will query the comments_likes association table
    db.session.commit()
# Send a new like notification to the comment author (need to automatically subtract 1)
    comment.author.add_notification('unread_comments_likes_count',
                                    comment.author.new_comments_likes())
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': 'You are not liking this comment anymore.'
    })
