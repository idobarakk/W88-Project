from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from flask_login import current_user
from wtforms import SelectField , StringField,PasswordField,SubmitField, BooleanField, IntegerField, DateTimeField, DateField, TimeField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from app.drugapi import DrugAPI


# *********** Login \ Register **************

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20) ])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username (self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That Username is taken. Choose a diffrent one.')
        
    def validate_email (self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Choose a diffrent one.')


class LoginForms(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember =BooleanField('Remember Me')
    submit = SubmitField('login')

# *********** Notifications **************

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20) ])
    email = StringField('Email',validators=[DataRequired(),Email()])
    picture = FileField("Update Profile Picture",validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')

    def validate_username (self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That Username is taken. Choose a diffrent one.')
        else:
            raise ValidationError('That Username must be diffrent than your current one.') 
            
    def validate_email (self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Choose a diffrent one.')
        else:
            raise ValidationError('That Username must be diffrent than your current one.')
        
        
class AddNotificationForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content',validators=[DataRequired()])
    date = DateField('Date',validators=[DataRequired()])
    time = TimeField('Time',validators=[DataRequired()])
    submit = SubmitField('Add Notification')

    def validate_date (self,date):
        if date.data <  datetime.utcnow().date():
            raise ValidationError('the date is not valid - please choose future date.')
        
    def validate_time (self,time):
        if time.data <  datetime.utcnow().time():
            raise ValidationError('the time is not valid- please choose future time.')

# *********** Drugs **************

class AddDrugForm(FlaskForm):
    name = StringField('Drug Name',validators=[DataRequired()])
    type = SelectField('Drug Type',validators=[DataRequired()],choices=[('pill', 'Pills'), ('drop', 'Drops'), ('liquid', 'Liquid (ml)')])
    dose = IntegerField('Dose (for Drops or Liquid - ml)',validators=[DataRequired()])
    timesaday = IntegerField('How many times a day?',validators=[DataRequired()])
    daystotake = IntegerField('How many days to take?',validators=[DataRequired()])
    startdate = DateField('Starting date',validators=[DataRequired()])
    taketime= TimeField('Take Time ',validators=[DataRequired()])
    gap = IntegerField('Gap between each take (hours)',validators=[DataRequired()])
    packsize = IntegerField('Pack Size?',validators=[DataRequired()])
    submit = SubmitField('Add Drug')

    def validate_name (self,name):
        current_drug = DrugAPI(name.data)
        durg_info = current_drug.check_fda_approval(current_drug.drug_name)
        if durg_info == None:
            raise ValidationError('Drug not found in FDA Data Base')

class AddActivityForm(FlaskForm):
    a1d1 = BooleanField('a1d1')
    a1d2 = BooleanField('a1d2')
    a1d3 = BooleanField('a1d3')
    a1d4 = BooleanField('a1d4')
    a1d5 = BooleanField('a1d5')
    a1d6 = BooleanField('a1d6')
    a1d7 = BooleanField('a1d7')
    a2d1 = BooleanField('a2d1')
    a2d2 = BooleanField('a2d2')
    a2d3 = BooleanField('a2d3')
    a2d4 = BooleanField('a2d4')
    a2d5 = BooleanField('a2d5')
    a2d6 = BooleanField('a2d6')
    a2d7 = BooleanField('a2d7')
    a3d1 = BooleanField('a3d1')
    a3d2 = BooleanField('a3d2')
    a3d3 = BooleanField('a3d3')
    a3d4 = BooleanField('a3d4')
    a3d5 = BooleanField('a3d5')
    a3d6 = BooleanField('a3d6')
    a3d7 = BooleanField('a3d7')
    submit = SubmitField('Add Activities')

