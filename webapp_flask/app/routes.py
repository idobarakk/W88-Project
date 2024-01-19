import secrets
import os
from PIL import Image
from flask import Flask, render_template, url_for,  flash, redirect, request,abort
from app.models import User, Post, Notification
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForms ,UpdateAccountForm, AddNotificationForm
from flask_login import login_user, current_user ,logout_user,login_required



#pages and website logic
@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.date.asc()).order_by(Notification.time.asc()).limit(3)
        return render_template("home.html",notifications=notifications)
    else:
        return render_template("home.html")


@app.route("/drugs")
@login_required
def drugs():
    return render_template("drugs.html")

@app.route("/edit_notification/<int:notification_id>",methods=['GET','POST'])
@login_required
def edit_notification(notification_id):
    form = AddNotificationForm()
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        abort(403)
    if form.validate_on_submit():
        notification.title = form.title.data
        notification.content = form.content.data
        notification.date = form.date.data
        notification.time = form.time.data
        db.session.commit()
        flash('Your Notification has been Updated !','success')
        return redirect(url_for('notification'))

    elif request.method == 'GET':
        form.title.data = notification.title
        form.content.data = notification.content  
        form.date.data = notification.date 
        form.time.data = notification.time
    return render_template("edit_notification.html", title="edit Notification", notification=notification, form=form)


@app.route("/delete_notification/<int:notification_id>", methods=['GET','POST'])
@login_required
def delete_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    print(notification)
    print(notification_id)
    db.session.delete(notification)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/add_notification",methods=['GET','POST'])
@login_required
def add_notification():
    form = AddNotificationForm()
    if form.validate_on_submit():
        notification = Notification(title=form.title.data,content=form.content.data,date=form.date.data,time=form.time.data,user_id=current_user.id)
        db.session.add(notification)
        db.session.commit()
        return redirect(url_for('notification'))
        flash('Your Notification has been added !','success')
    return render_template("add_notification.html", title="Add Notification", form=form)


@app.route("/notification")
@login_required
def notification():
    if current_user.is_authenticated:
        notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.date.asc()).order_by(Notification.time.asc())
        return render_template("notification.html",notifications=notifications, title="Notification")
    else:
        return render_template("home.html")


@app.route("/api")
def api():
    data = request.json
    if not data:
        return "no data sent"
    return [data,data]


@app.route("/about")
@login_required
def about():
    return render_template("about.html")


@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():

        hased_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hased_pw)
        
        db.session.add(user)
        db.session.commit()
        flash('Your account has been Created !','success')
        return redirect(url_for('login'))
    return render_template("register.html",  title="Register", form=form)


@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForms()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('email or pass are worng- try again', 'danger')
    return render_template("login.html",  title='Login', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    rnd_hex = secrets.token_hex(8)
    _, f_ext =os.path.splitext(form_picture.filename)
    picture_fn = rnd_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics',picture_fn)

    #resize
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn





@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has bee updated','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file= url_for('static',filename = 'profile_pics/'+ current_user.image_file)
    return render_template("account.html",  title='Account', image_file=image_file , form=form)
