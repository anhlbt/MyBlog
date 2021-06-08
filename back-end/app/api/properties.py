from flask import request, jsonify, url_for, g, current_app, send_from_directory
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response, bad_request
from app.extensions import db
from app.models import Permission, Property, Comment
from app.utils.decorator import permission_required
from app.utils import img_util
import pdb
import os,datetime
from werkzeug.utils import secure_filename
import uuid
from flask_cors import cross_origin
# from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import array, ARRAY
from sqlalchemy import tuple_, cast
from os.path import dirname, join
import base64



APP_ROOT = dirname(dirname(dirname(__file__)))
UPLOAD_FOLDER = join(APP_ROOT, 'uploads')

# properties
# @token_auth.login_required
@bp.route('/static/<string:path>')
def serve_js(path):
    # with open(join(UPLOAD_FOLDER, path), 'rb') as f:
    #     im_b64 = base64.b64encode(f.read())
    
    return send_from_directory(UPLOAD_FOLDER, path)
    # return im_b64


@bp.route('/properties/', methods=['POST'])
@token_auth.login_required
@permission_required(Permission.WRITE)
def create_property():
    # pdb.set_trace()
    data = request.get_json()
    if not data:
        return bad_request('You must property JSON data.')
    message = {}
    if 'title' not in data or not data.get('title').strip():
        message['title'] = 'Title is required.'
    elif len(data.get('title')) > 255:
        message['title'] = 'Title must less than 255 characters.'
    if 'description' not in data or not data.get('description').strip():
        message['description'] = 'description is required.'
    if message:
        return bad_request(message)

    property = Property()
    property.from_dict(data)
    property.author = g.current_user 
    db.session.add(property)

    ##  no need send notification to followers
    # for user in property.author.followers:
    #     user.add_notification('unread_followeds_properties_count',
    #                           user.new_followeds_properties())
    db.session.commit()
    response = jsonify(property.to_dict())
    response.status_code = 201
    #The HTTP protocol requires the 201 response to contain a Location header whose value is the URL of the new resource
    response.headers['Location'] = url_for('api.get_property', id=property.id)
    return response

#Upload
@bp.route('/upload/',methods=['POST','GET'])
@cross_origin(origin='*')
@token_auth.login_required
@permission_required(Permission.WRITE)
def uploadFile():
    if request.method == 'POST':
        try:
            files = request.files.getlist("file")
            lst_files = []
            if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
                os.makedirs(current_app.config['UPLOAD_FOLDER'])
            for file in files:
                if file and img_util.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Gen GUUID File Name
                    fileExt = filename.split('.')[1]
                    autoGenFileName = uuid.uuid4()
                    newFileName = str(autoGenFileName) + '.' + fileExt
                    
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], newFileName))
                    lst_files.append(newFileName)
            return jsonify(lst_files)
        except Exception as ex:
            print(ex)
            return "something went wrong"
        # return redirect(url_for('result'))

def lst2pgarr(alist):
    return '{' + ','.join(alist) + '}'

@bp.route('/properties_area/', methods=['GET','POST'])
@cross_origin(origin='*')
def get_properties_by_area():
    try:    
        data = request.get_json()
        if not data:
            return bad_request('You must property JSON data.')
        province = data.get('province')
        district = data.get('district')
        ward = data.get('ward')
        _type = data.get('type')
        purpose = data.get('purpose')
        floor = data.get('floor')
        bedroom = data.get('bedroom')
        bathroom = data.get('bathroom')
        agency = data.get('bathroom')
        agent = data.get('agent')
        checked = data.get('checked')
        features = data.get('features')
        price = data.get('price')
        max_price = 5000000
        min_price = 1000000
        direction = data.get('direction')
        print(ward, district, province)
        print('data', data)
        base_query = None
        if purpose: 
            base_query = Property.query.filter(Property.purpose == purpose)

        if province:
            base_query = base_query.filter(Property.province == province)
            if district:
                base_query = base_query.filter(Property.district==district)
                if ward:
                    base_query = base_query.filter(Property.ward==ward)
                    
        if _type: 
            print("type, " ,_type)
            base_query = base_query.filter(Property.type == _type)            
        if floor: 
            print("floor ", floor)
            base_query = base_query.filter(Property.floor== floor) 
        if bedroom:
            print("bedroom", bedroom)
            base_query = base_query.filter(Property.bedroom ==bedroom)   
        # if bathroom:
        #     base_query = base_query.filter(Property.bathroom == bathroom)    
        # if agent:
        #     base_query = base_query.filter(Property.agent == agent) 
        # if agency:
        #     base_query = base_query.filter(Property.agency == agency)
        # if checked:
        #     base_query = base_query.filter(Property.checked == checked)
        # if max_price and min_price:
        #     base_query = base_query.filter(Property.price >= min_price, Property.price <= max_price)               
        if direction:
            base_query = base_query.filter(Property.direction == direction)        
        if features:
            features = lst2pgarr(features)
            base_query = base_query.filter(Property.features == features)  
            # base_query = base_query.filter(Property.features=='{"barbeque", "airconditioning"}')   
 
        print(" len of data", len(base_query.all()))
        result = Property.to_collection_dict(base_query, 1, 5,'api.get_properties_by_area')
        print(result)
        return jsonify(result)
    except Exception as ex:
        print(ex)

@bp.route('/subdivisions/<int:id>', methods=['GET'])
@token_auth.login_required
def get_subdivisions(id):
    if id % 10000 == 0:
        print("province: ", id)
    elif id % 100 == 0:
        print("district: ", id)
        print("province: ", (id //10000)*10000)
    else:
        print("ward: ", id)
        print("district: ",  (id //100)*100)
        print("province: ", (id //10000)*10000)
    



@bp.route('/properties/', methods=['GET'])
def get_properties():
    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)
    
    data = Property.to_collection_dict(
        Property.query.order_by(Property.created_at.desc()), page, per_page, 'api.get_properties')
    return jsonify(data)

# #get properties by topic
# @bp.route('/properties/<topic>', methods=['GET'])
# def get_property_by_topic(topic):
#     page = request.args.get('page', 1, type=int)
#     per_page = min(
#         request.args.get(
#             'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)
#     data = Property.to_collection_dict(Property.query.filter(Property.topic == topic), page, per_page, 'api.get_property_by_topic', topic=topic)
#     return jsonify(data)


@bp.route('/properties/<int:id>', methods=['GET'])
def get_property(id):
    '''Return to an article'''
    property = Property.query.get_or_404(id)
    property.views += 1
    db.session.add(property)
    db.session.commit()
    data = property.to_dict()
    # Next article
    next_basequery = Property.query.order_by(Property.created_at.desc()).filter(Property.created_at > property.created_at)
    if next_basequery.all():
        data['next_id'] = next_basequery[-1].id
        data['next_title'] = next_basequery[-1].title
        data['_links']['next'] = url_for('api.get_property', id=next_basequery[-1].id)
    else:
        data['_links']['next'] = None
    # Previous article
    prev_basequery = Property.query.order_by(Property.created_at.desc()).filter(Property.created_at < property.created_at)
    if prev_basequery.first():
        data['prev_id'] = prev_basequery.first().id
        data['prev_title'] = prev_basequery.first().title
        data['_links']['prev'] = url_for('api.get_property', id=prev_basequery.first().id)
    else:
        data['_links']['prev'] = None
    return jsonify(data)


@bp.route('/properties/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_property(id):
    '''Edit an article'''
    property = Property.query.get_or_404(id)
    if g.current_user != property.author and not g.current_user.can(Permission.ADMIN):
        return error_response(403)

    data = request.get_json()
    # print(data)
    # pdb.set_trace()
    if not data:
        return bad_request('You must property JSON data.')
    message = {}
    if 'title' not in data or not data.get('title').strip():
        message['title'] = 'Title is required.'
    elif len(data.get('title')) > 255:
        message['title'] = 'Title must less than 255 characters.'
    if 'description' not in data or not data.get('description').strip():
        message['body'] = 'Description is required.'
    if message:
        return bad_request(message)

    property.from_dict(data)
    db.session.commit()
    return jsonify(property.to_dict())


@bp.route('/properties/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_property(id):
    '''删除一篇文章'''
    property = Property.query.get_or_404(id)
    if g.current_user != property.author and not g.current_user.can(Permission.ADMIN):
        return error_response(403)
    db.session.delete(property)
    # 给文章作者的所有粉丝发送新文章通知(需要自动减1)
    for user in property.author.followers:
        user.add_notification('unread_followeds_properties_count',
                              user.new_followeds_properties())
    db.session.commit()
    return '', 204


@bp.route('/properties/<int:id>/like', methods=['GET'])
@token_auth.login_required
def like_property(id):
    '''Like article'''
    property = Property.query.get_or_404(id)
    property.liked_by(g.current_user)
    db.session.add(property)
    # Remember to submit first, first add the likes record to the database, because new_properties_likes() will query the properties_likes association table
    db.session.commit()
    # Send new like notifications to article authors
    property.author.add_notification('unread_properties_likes_count',
                                 property.author.new_properties_likes())
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': 'You are now liking this property.'
    })


@bp.route('/properties/<int:id>/unlike', methods=['GET'])
@token_auth.login_required
def unlike_property(id):
    '''Unlike article'''
    property = Property.query.get_or_404(id)
    property.unliked_by(g.current_user)
    db.session.add(property)
    # 切记要先提交，先添加喜欢记录到数据库，因为 new_properties_likes() 会查询 properties_likes 关联表
    db.session.commit()
    # 给文章作者发送新喜欢通知(需要自动减1)
    property.author.add_notification('unread_properties_likes_count',
                                 property.author.new_properties_likes())
    db.session.commit()
    return jsonify({
        'status': 'success',
        'message': 'You are not liking this property anymore.'
    })


@bp.route('/properties/export-properties/', methods=['GET'])
@token_auth.login_required
@permission_required(Permission.WRITE)
def export_properties():
    '''Export all articles of the current user, RQ background tasks'''
    if g.current_user.get_task_in_progress('export_properties'):  # 如果用户已经有同名的后台任务在运行中时
        return bad_request('The background task of the last exported article has not ended')
    else:
        # 将 app.utils.tasks.export_properties 放入任务队列中
        g.current_user.launch_task('export_properties', 'Exporting articles...', kwargs={'user_id': g.current_user.id})
        return jsonify(message='Background task for exporting articles is running')


###
# research all
###
@bp.route('/search_properties/', methods=['GET'])
def search_properties():
    '''Elasticsearch full-text search blog post'''
    q = request.args.get('q')
    if not q:
        return bad_request(message='keyword is required.')

    page = request.args.get('page', 1, type=int)
    per_page = min(
        request.args.get(
            'per_page', current_app.config['POSTS_PER_PAGE'], type=int), 100)

    total, hits_basequery = Property.search(q, page, per_page)
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
            'self': url_for('api.search_properties', q=q, page=page, per_page=per_page),
            'next': url_for('api.search_properties', q=q, page=page + 1, per_page=per_page) if page < total_pages else None,
            'prev': url_for('api.search_properties', q=q, page=page - 1, per_page=per_page) if page > 1 else None
        }
    }
    return jsonify(data=data, message='Total items: {}, current page: {}'.format(total, page))


@bp.route('/search_properties/property-detail/<int:id>', methods=['GET'])
def get_search_property(id):
    '''Jump to article details from the search result list page'''
    q = request.args.get('q')
    page = request.args.get('page', type=int)
    per_page = request.args.get('per_page', type=int)

    if q and page and per_page:  # 说明是从搜索结果页中过来查看文章详情的，所以要高亮关键字
        total, hits_basequery = Property.search(q, page, per_page)
        property = hits_basequery.first()  # 只会有唯一的一篇文章
        data = property.to_dict()  # 会高亮关键字
    else:
        property = Property.query.get_or_404(id)
        data = property.to_dict()  # 不会高亮关键字

    # 下一篇文章
    next_basequery = Property.query.order_by(Property.created_at.desc()).filter(Property.created_at > property.created_at)
    if next_basequery.all():
        data['next_id'] = next_basequery[-1].id
        data['next_title'] = next_basequery[-1].title
        data['_links']['next'] = url_for('api.get_property', id=next_basequery[-1].id)
    else:
        data['_links']['next'] = None
    # 上一篇文章
    prev_basequery = Property.query.order_by(Property.created_at.desc()).filter(Property.created_at < property.created_at)
    if prev_basequery.first():
        data['prev_id'] = prev_basequery.first().id
        data['prev_title'] = prev_basequery.first().title
        data['_links']['prev'] = url_for('api.get_property', id=prev_basequery.first().id)
    else:
        data['_links']['prev'] = None
    return jsonify(data)
