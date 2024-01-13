from flask import Flask, render_template, url_for,  flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForms
from datetime import datetime


#Create our TakeCare App
app = Flask(__name__)

#configure rnadom secret key and db location
app.config['SECRET_KEY'] = '47db71e739639f70b97f57093694bbec'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

#create Databse related to the app
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True,nullable=False)
    email = db.Column(db.String(100), unique=True,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    password= db.Column(db.String(60),nullable=False)
    posts =db.relationship('Post',backref='autor',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.Date,nullable=False,default=datetime.utcnow())
    cotent = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"


#pages and website logic
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/api")
def api():
    data = request.json
    if not data:
        return "no data sent"
    return [data,data]


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account Created !','success')
        return redirect(url_for('home'))
    return render_template("register.html",  title="register", form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForms()
    if form.validate_on_submit():
        if form.email.data == 'admin@takecare.com' and form.password.data == 'password':
            flash('you are logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('email or pass are worng- try again', 'danger')

    return render_template("login.html",  title='login', form=form)

if __name__ =='__main__':
    app.run(debug=True)