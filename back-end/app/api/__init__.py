from flask import Blueprint

bp = Blueprint('api', __name__)

# Written at the end to prevent circular import, ping.py file will also import bp
from app.api import ping, tokens, errors, roles, users, posts, properties, comments, notifications, messages
