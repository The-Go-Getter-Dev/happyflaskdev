from flask import Flask, render_template,request
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_marshmallow import Marshmallow

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
ma = Marshmallow()
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    #here by bulprint we are going to to add the routes
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # adding api bllur prints with url getcult/apiV1.0
    from .api import api as api_bp
    app.register_blueprint(api_bp, url_prefix='/getcult/apiV1.0/')
    
    
    # attach routes and custom error pages here
    return app

