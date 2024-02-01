import secrets
import os
from PIL import Image
from flask import Flask, render_template, url_for,  flash, redirect, request,abort
from app.models import User, Notification ,Drug, DrugSchedule,Activities,Elderlyuser
from app import app, db, bcrypt ,socketio
from app.forms import RegistrationForm, LoginForms ,UpdateAccountForm, AddNotificationForm ,AddDrugForm,AddActivityForm
from flask_login import login_user, current_user ,logout_user,login_required
from app.drugapi import DrugAPI
from datetime import timedelta,datetime,time
import json



#pages and website logic
@app.route("/")
@app.route("/home")
@login_required
def home():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.date.asc()).order_by(Notification.time.asc()).limit(3)
    drugs = Drug.query.filter_by(user_id=current_user.id)
    eldelys = Elderlyuser.query.filter_by(user_id=current_user.id)
    eldelys_dict = {i.id: i.username for i in eldelys}
    return render_template("home.html",notifications=notifications ,drugs=drugs,eldelys_dict=eldelys_dict)



@app.route("/drugs")
@login_required
def drugs():
    if current_user.is_authenticated:
        drugs = Drug.query.filter_by(user_id=current_user.id)
        drug_schedule = DrugSchedule.query.filter_by(user_id=current_user.id)
        eldelys = Elderlyuser.query.filter_by(user_id=current_user.id)
        eldelys_dict = {i.id: i.username for i in eldelys}
        return render_template("drugs.html",drugs=drugs,drug_schedule=drug_schedule, title="Drugs",eldelys_dict=eldelys_dict)
    else:
        return render_template("home.html")
    


def calc_dates(drug):
    drug_id = drug.id
    startdate = drug.startdate
    gap = drug.gap
    taketime = drug.taketime
    packsize = drug.packsize
    timesaday = drug.timesaday
    dose = drug.dose
    daystotake = drug.daystotake

    datelist = []
    timelist =[]

    dummy_date = datetime(2000, 1, 1)  # Dummy date
    taketime_datetime = datetime.combine(dummy_date, taketime)

    timelist.append(taketime)
    while timesaday > 1:
        taketime_datetime = taketime_datetime + timedelta(hours=gap)
        timelist.append(taketime_datetime.time())
        timesaday -= 1

    datelist.append(startdate)
    while daystotake > 1:
        startdate = startdate + timedelta(days=1)
        datelist.append(startdate)
        daystotake -= 1

    return datelist,timelist





@app.route("/add_drug",methods=['GET','POST'])
@login_required
def add_drug():
    eldelys = Elderlyuser.query.filter_by(user_id=current_user.id)
    eldelys_list = [(i.id,i.username) for i in  eldelys ]
    form = AddDrugForm()
    form.eldrly.choices = eldelys_list
    if form.validate_on_submit():
        drug = Drug(name=form.name.data,type=form.type.data,dose=form.dose.data,timesaday=form.timesaday.data,daystotake=form.daystotake.data,user_id=current_user.id,startdate=form.startdate.data,packsize=form.packsize.data,gap=form.gap.data,taketime=form.taketime.data,elderly_user_id=form.eldrly.data)
        db.session.add(drug)
        db.session.commit()
        drug = Drug.query.filter_by(user_id=current_user.id).order_by(Drug.id.desc()).first()
        dateslist, timeslist = calc_dates(drug)
        for date in dateslist:
            for time in timeslist:
                drug_schedule = DrugSchedule(user_id=current_user.id,drug_id=drug.id,takedate=date,taketime=time,took=False,elderly_user_id=form.eldrly.data)
                db.session.add(drug_schedule)
                db.session.commit()

        flash('Your Drug has been added !','success')
        return redirect(url_for('drugs'))
        
    return render_template("add_drug.html", title="Add Drug", form=form,eldelys_list=eldelys_list)


@app.route("/delete_drug/<int:drug_id>", methods=['GET','POST'])
@login_required
def delete_drug(drug_id):

    drug = Drug.query.get_or_404(drug_id)
    db.session.delete(drug)
    db.session.commit()

    flash('Your drug has been deleted!', 'success')
    return redirect(url_for('drugs'))


@app.route("/edit_notification/<int:notification_id>",methods=['GET','POST'])
@login_required
def edit_notification(notification_id):
    eldelys = Elderlyuser.query.filter_by(user_id=current_user.id)
    eldelys_list = [(i.id, i.username) for i in eldelys]
    form = AddNotificationForm()
    form.eldrly.choices = eldelys_list
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        abort(403)
    if form.validate_on_submit():
        notification.title = form.title.data
        notification.content = form.content.data
        notification.date = form.date.data
        notification.time = form.time.data
        notification.elderly_user_id = form.eldrly.data
        db.session.commit()
        flash('Your Notification has been Updated !','success')
        return redirect(url_for('notification'))

    elif request.method == 'GET':
        form.title.data = notification.title
        form.content.data = notification.content  
        form.date.data = notification.date 
        form.time.data = notification.time
        form.eldrly.data = notification.elderly_user_id
    return render_template("edit_notification.html", title="edit Notification", notification=notification, form=form,eldelys_list=eldelys_list)


@app.route("/delete_notification/<int:notification_id>", methods=['GET','POST'])
@login_required
def delete_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    print(notification)
    print(notification_id)
    db.session.delete(notification)
    db.session.commit()
    flash('Your notification has been deleted!', 'success')
    return redirect(url_for('notification'))


@app.route("/add_notification",methods=['GET','POST'])
@login_required
def add_notification():
    eldelys = Elderlyuser.query.filter_by(user_id=current_user.id)
    eldelys_list = [(i.id,i.username) for i in  eldelys ]
    form = AddNotificationForm()
    form.eldrly.choices = eldelys_list
    if form.validate_on_submit():
        notification = Notification(title=form.title.data,content=form.content.data,date=form.date.data,time=form.time.data,user_id=current_user.id,elderly_user_id=form.eldrly.data)
        db.session.add(notification)
        db.session.commit()
        return redirect(url_for('notification'))
        flash('Your Notification has been added !','success')
    return render_template("add_notification.html", title="Add Notification", form=form ,eldelys_list=eldelys_list)


@app.route("/notification")
@login_required
def notification():
    if current_user.is_authenticated:
        notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.date.asc()).order_by(Notification.time.asc())
        eldelys = Elderlyuser.query.filter_by(user_id=current_user.id)
        eldelys_dict = {i.id: i.username for i in eldelys}
        return render_template("notification.html",notifications=notifications,eldelys_dict=eldelys_dict, title="Notification")
    else:
        return render_template("home.html")


@app.route("/api", methods=['GET','POST'])
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
        elderly_hased_pw = bcrypt.generate_password_hash(form.elderlypassword.data).decode('utf-8')
        if form.elderlypassword.data:
            elderly2_hased_pw = bcrypt.generate_password_hash(form.elderlypassword2.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hased_pw)
        db.session.add(user)
        db.session.commit()
        elderly_user = Elderlyuser(username=form.elderlyusername.data, password=elderly_hased_pw, user_id=user.id)
        db.session.add(elderly_user)
        db.session.commit()
        if form.elderlypassword.data:
            elderly2_hased_pw = bcrypt.generate_password_hash(form.elderlypassword2.data).decode('utf-8')
            elderly_user2 = Elderlyuser(username=form.elderlyusername2.data, password=elderly2_hased_pw, user_id=user.id)
            db.session.add(elderly_user2)
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



@app.route('/send_message')
def send_message():
    message = "Hello from Flask!"
    socketio.emit('my_message', {'data': message})
    return "Message sent!"



@app.route("/activities")
@login_required
def activities():
    if current_user.is_authenticated:
        activities = Activities.query.filter_by(user_id=current_user.id)
        return render_template("activities.html",activities=activities, title="activities")
    else:
        return render_template("home.html")
    

@app.route("/add_activity",methods=['GET','POST'])
@login_required
def add_activity():

    eldelys = Elderlyuser.query.filter_by(user_id=current_user.id)
    eldelys_list = [(i.id, i.username) for i in eldelys]
    form = AddActivityForm()
    form.eldrly.choices = eldelys_list
    if form.validate_on_submit():
        activity = Activities(day=1,activity1=form.a1d1.data,activity2=form.a2d1.data,activity3=form.a3d1.data,user_id=current_user.id,elderly_user_id=form.eldrly.data)
        db.session.add(activity)
        activity = Activities(day=2,activity1=form.a1d2.data,activity2=form.a2d2.data,activity3=form.a3d2.data,user_id=current_user.id,elderly_user_id=form.eldrly.data)
        db.session.add(activity)
        activity = Activities(day=3,activity1=form.a1d3.data,activity2=form.a2d3.data,activity3=form.a3d3.data,user_id=current_user.id,elderly_user_id=form.eldrly.data)
        db.session.add(activity)
        activity = Activities(day=4,activity1=form.a1d4.data,activity2=form.a2d4.data,activity3=form.a3d4.data,user_id=current_user.id,elderly_user_id=form.eldrly.data)
        db.session.add(activity)
        activity = Activities(day=5,activity1=form.a1d5.data,activity2=form.a2d5.data,activity3=form.a3d5.data,user_id=current_user.id,elderly_user_id=form.eldrly.data)
        db.session.add(activity)
        activity = Activities(day=6,activity1=form.a1d6.data,activity2=form.a2d6.data,activity6=form.a3d6.data,user_id=current_user.id,elderly_user_id=form.eldrly.data)
        db.session.add(activity)
        activity = Activities(day=7,activity1=form.a1d7.data,activity2=form.a2d7.data,activity3=form.a3d7.data,user_id=current_user.id,elderly_user_id=form.eldrly.data)
        db.session.add(activity)
        db.session.commit()
        drug = Drug.query.filter_by(user_id=current_user.id).order_by(Drug.id.desc()).first()
        dateslist, timeslist = calc_dates(drug)
        flash('Your Activity has been added !', 'success')
        return redirect(url_for('activities'))
    return render_template("add_activity.html", title="Add Activity", form=form)


# @socketio.on('message')
# def message(data):
#     print(data)
#     socketio.emit('message', data)
#     login_user(data)
#     #print('received message: ' + data)
#     #current_drug = DrugAPI(data)
#     #drug_info = current_drug.check_fda_approval(current_drug.drug_name)
#     #print(drug_info)
#
#     #socketio.emit('message', {'message': 'this is data from the flask '+str(drug_info)})
#     return "Message sent!"

@socketio.on('message')
def message(data):
    try:
        # If 'data' is a JSON string, convert it to a dictionary
        data_dict = json.loads(data)
    except json.JSONDecodeError:
        # If 'data' is not a valid JSON string, handle the error
        print("Received data is not in JSON format:", data)
        return "Invalid data format"

    # Now you can safely use the get method on the dictionary
    user_email_or_username = data_dict.get("email_or_username")
    user = User.query.filter_by(email=user_email_or_username).first()  # or username
    if current_user.is_authenticated:

        drug = DrugSchedule.query.filter_by(user_id=current_user.id).all()
        socketio.emit('message', {'message': str(drug)})
    if user:
        login_user(user)
        socketio.emit('message', {'message': 'User logged in'})
    else:
        socketio.emit('message', {'message': 'User not found'})

    return "Message processed!"