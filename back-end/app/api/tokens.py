from flask import jsonify, g
from app.api import bp
from app.api.auth import basic_auth
from app.extensions import db


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_jwt()
    # Every time a user logs in (ie after successfully obtaining JWT), update the last_seen time
    g.current_user.ping()
    db.session.commit()
    return jsonify({'token': token})
