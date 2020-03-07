import os 
from flask import Flask
from APP.views import init_blue, init_login
from APP.models import init_db
from flask_bootstrap import Bootstrap


def create_app():
    app = Flask(__name__)
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =SQLALCHEMY_TRACK_MODIFICATIONS


    init_blue(app)
    init_db(app)
    Bootstrap(app)
    init_login(app)
 

   

    return app