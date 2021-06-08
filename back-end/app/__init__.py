import logging
from logging.handlers import RotatingFileHandler
import os
from elasticsearch import Elasticsearch
from redis import Redis
import rq
from flask import Flask, request
from app.api import bp as api_bp
from app.api_v2.app import bp as api_v2_bp
from app.extensions import cors, db, migrate, mail, babel
import ssl
from flask_sslify import SSLify

def create_app(config_class=None):
    '''Factory Pattern: Create Flask app.'''
    app = Flask(__name__)
    # sslify = SSLify(app)
    # Initialization flask app
    configure_app(app, config_class)
    configure_blueprints(app)
    configure_extensions(app)
    configure_logging(app)
    # 不使用 Jinja2，用不到模版过滤器和上下文处理器
    # configure_template_filters(app)
    # configure_context_processors(app)
    configure_before_handlers(app)
    configure_after_handlers(app)
    configure_errorhandlers(app)

    return app


def configure_app(app, config_class):
    # app.ssl_context=('../cert.pem', '../key.pem')
    app.config.from_object(config_class)
    # Do not check if there is a slash at the end of the route /
    app.url_map.strict_slashes = False
    # intergrate RQ task queue
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    # set the maximum execution timeout for each task in the task queue to be 1 hour
    app.task_queue = rq.Queue('madblog-tasks', connection=app.redis, default_timeout=3600)  # 
    # Elasticsearch full text
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None


def configure_blueprints(app):
    # Register blueprint
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(api_v2_bp, url_prefix='/api/v2')


def configure_extensions(app):
    '''Configures the extensions.'''
    # Enable CORS
    cors.init_app(app)
    # Init Flask-SQLAlchemy
    db.init_app(app)
    # Init Flask-Migrate
    migrate.init_app(app, db)
    # Init Flask-Mail
    mail.init_app(app)
    # Init Flask-Babel
    babel.init_app(app)

    @babel.localeselector
    def get_locale():
        # return 'zh'  # with this setting all users will always display this language (vn, zh, en...)
        return request.accept_languages.best_match(app.config['LANGUAGES'])


def configure_logging(app):
    '''Configure Logging.'''
    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/madblog.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask API Startup')


def configure_before_handlers(app):
    '''Configures the before request handlers'''
    pass


def configure_after_handlers(app):
    '''Configures the after request handlers'''
    pass


def configure_errorhandlers(app):
    '''Configures the error handlers'''
    pass
