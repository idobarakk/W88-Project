from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_socketio import SocketIO

#Create our TakeCare App
app = Flask(__name__)

#configure rnadom secret key and db location
app.config['SECRET_KEY'] = '47db71e739639f70b97f57093694bbec'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

#create Databse related to the app
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
admin = Admin(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category ='info'
socketio = SocketIO(app,logger=True, engineio_logger=True)


from app import models


#to see the relationship - need create view
class NotificationView(ModelView):
    column_display_pk = True 
    column_hide_backrefs = False
    column_list = ('id', 'title', 'content','date','time','user_id')


admin.add_view(ModelView(models.User, db.session))
admin.add_view(NotificationView(models.Notification, db.session))

## one time creation
with app.app_context() as ctx:
    ctx.push()
    db.create_all()

from app import routes
