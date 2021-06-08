from flask import Blueprint
from flask_restful import Api


# Blueprint
bp = Blueprint('api_v2', __name__)
# Init Flask-RESTful
api = Api(bp)

# Unified registration routing
from app.api_v2 import urls
