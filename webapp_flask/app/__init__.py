from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#Create our TakeCare App
app = Flask(__name__)

#configure rnadom secret key and db location
app.config['SECRET_KEY'] = '47db71e739639f70b97f57093694bbec'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

#create Databse related to the app
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category ='info'


from app import models

## one time creation
with app.app_context() as ctx:
    ctx.push()
    db.create_all()

from app import routes