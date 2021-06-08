from flask import request, url_for, jsonify
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.extensions import db
from app.models import Role
from app.utils.decorator import admin_required


@bp.route('/roles/perms', methods=['GET'])
def get_perms():
    '''Get all Permissions'''
    data = [
        {'name': 'FOLLOW', 'dec': 1},
        {'name': 'COMMENT', 'dec': 2},
        {'name': 'WRITE', 'dec': 4},
        {'name': 'ADMIN', 'dec': 128}
    ]
    return jsonify(data)


@bp.route('/roles', methods=['POST'])
@token_auth.login_required
@admin_required
def create_role():
    '''Register a new role'''
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')

    message = {}
    if 'slug' not in data or not data.get('slug', None).strip():
        message['slug'] = 'Please provide a valid slug.'
    if 'name' not in data or not data.get('name', None).strip():
        message['name'] = 'Please provide a valid name.'

    if Role.query.filter_by(slug=data.get('slug', None)).first():
        message['slug'] = 'Please use a different slug.'
    if message:
        return bad_request(message)

    permissions = 0
    for perm in data.get('permissions', 0):
        permissions += perm
    data['permissions'] = permissions

    role = Role()
    role.from_dict(data)
    db.session.add(role)
    db.session.commit()

    response = jsonify(role.to_dict())
    response.status_code = 201
    # The HTTP protocol requires the 201 response to contain a Location header whose value is the URL of the new resource
    response.headers['Location'] = url_for('api.get_role', id=role.id)
    return response


@bp.route('/roles', methods=['GET'])
@token_auth.login_required
@admin_required
def get_roles():
    '''Returns the collection of all characters'''
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Role.to_collection_dict(Role.query, page, per_page, 'api.get_roles')
    return jsonify(data)


@bp.route('/roles/<int:id>', methods=['GET'])
@token_auth.login_required
@admin_required
def get_role(id):
    '''Return a character'''
    role = Role.query.get_or_404(id)
    data = role.to_dict()

    # List of operation permissions that the current role has (list of integers)
    choices = [
        {'name': 'FOLLOW', 'dec': 1},
        {'name': 'COMMENT', 'dec': 2},
        {'name': 'WRITE', 'dec': 4},
        {'name': 'ADMIN', 'dec': 128}
    ]
    new_choices = filter(lambda x: role.has_permission(x['dec']), choices)
    data['perms'] = [x['dec'] for x in new_choices]
    return jsonify(data)


@bp.route('/roles/<int:id>', methods=['PUT'])
@token_auth.login_required
@admin_required
def update_role(id):
    '''Modify a role'''
    role = Role.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')

    message = {}
    if 'slug' not in data or not data.get('slug', None).strip():
        message['slug'] = 'Please provide a valid slug.'
    if 'name' not in data or not data.get('name', None).strip():
        message['name'] = 'Please provide a valid name.'

    r = Role.query.filter_by(slug=data.get('slug', None)).first()
    if r and r.id != role.id:
        message['slug'] = 'Please use a different slug.'
    if message:
        return bad_request(message)

    permissions = 0
    for perm in data.get('permissions', 0):
        permissions += perm
    data['permissions'] = permissions

    role.from_dict(data)
    db.session.commit()
    return jsonify(role.to_dict())


@bp.route('/roles/<int:id>', methods=['DELETE'])
@token_auth.login_required
@admin_required
def delete_role(id):
    '''Delete a role'''
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    return '', 204
