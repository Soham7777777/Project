from flask import Flask, redirect, render_template, url_for, flash
from flask_jwt_extended import JWTManager
from instance import IApplicationConfiguration
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_mail import Mail
import os
from celery import Celery, Task

class Base(MappedAsDataclass, DeclarativeBase):
    pass


db: SQLAlchemy = SQLAlchemy(model_class=Base)
login_manager: LoginManager = LoginManager()
mail = Mail()
jwt = JWTManager()


# def celery_init_app(app: Flask) -> Celery:
#     class FlaskTask(Task):
#         def __call__(self, *args: object, **kwargs: object) -> object:
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery_app = Celery(app.name, task_cls=FlaskTask)
#     celery_app.config_from_object(app.config["CELERY"])
#     celery_app.set_default()
#     app.extensions["celery"] = celery_app
#     return celery_app


def create_app(config: IApplicationConfiguration, /) -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    
    mail.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    # celery_init_app(app)
    from Application.models import User
    with app.app_context():
        db.create_all()

    from Application.blueprints import auth, account
    app.register_blueprint(auth.bp)
    app.register_blueprint(account.bp)

    def handle_unauthorized():
        flash("You are not authorized, please login", 'info')
        return redirect(url_for('Auth.login'))

    login_manager.unauthorized_handler(handle_unauthorized)
    
    @app.get('/')
    def home():
        if current_user.is_authenticated:
            return redirect(url_for('Account.dashboard'))
        return redirect(url_for('Auth.login'))

    if app.debug == True:
        with app.app_context():
            from instance import mock_db
            mock_db.populate_db(db)
            
    return app


MIN_NAME_SIZE=int(os.getenv('MIN_NAME_SIZE', 'None')) 
MAX_NAME_SIZE=int(os.getenv('MAX_NAME_SIZE', 'None'))
NAME_CAN_CONTAIN=os.getenv('NAME_CAN_CONTAIN', '')
MIN_PASSWORD_SIZE=int(os.getenv('MIN_PASSWORD_SIZE', 'None'))
MAX_PASSWORD_SIZE=int(os.getenv('MAX_PASSWORD_SIZE', 'None'))
PASSWORD_CAN_CONTAIN=os.getenv('PASSWORD_CAN_CONTAIN', '')
CONFIRMATION_LINK_EXPIRES_IN_X_MINUTES=float(os.getenv('CONFIRMATION_LINK_EXPIRES_IN_X_MINUTES', 'None'))