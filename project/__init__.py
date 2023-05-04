import logging as lg
from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

from werkzeug.security import generate_password_hash




# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

from .models import User
from .migrations import *


# def create_app():

app = Flask(__name__)
app.config.from_object('config')        # pour que l'appli puisse reconnaitre le fichier config

db.init_app(app)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Seans-Python-Flask-REST-Boilerplate"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL) 

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='192.168.1.104', port=4444, debug=True, threaded=False)

login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.init_app(app)


# Pour que 'current_user' puisse fonctionner 
@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


@app.cli.command()
def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    lg.warning('Database initialized!')

@app.cli.command()
def dev_migration():
    UserMigration.migrate()
    SellerMigration.migrate()
    CardTypeMigration.migrate()
    BalanceMigration.migrate()
    AddressMigration.migrate()
    # DeliveryZoneMigration.migrate()
    CategoryMigration.migrate()
    PromotionMigration.migrate()
    ProductMigration.migrate()
    ProductAndCAtegoryMigration.migrate()
    DeliveryToolTypeMigration.migrate()
    NotificationTypeMigration.migrate()
    PaymentMethodMigration.migrate()
    lg.warning("Data initialize for developpement")

@app.cli.command()
def api_generate():
    with open("project"+API_URL, "w") as f:
        json.dump(swagger(app), f, indent=4)
    lg.warning("API generate successfuly at {}".format(API_URL))

# blueprint for auth routes in our app
from .api.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .api.user import user as user_blueprint
app.register_blueprint(user_blueprint)

# blueprint for non-auth parts of app
from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)

# # blueprint for non-auth parts of app
# from .admin import admin as admin_blueprint
# app.register_blueprint(admin_blueprint)

# return app
