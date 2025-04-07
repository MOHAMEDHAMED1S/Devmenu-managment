from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional, URL
from app.models.user import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=20)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    contact_info = StringField('Contact Information', validators=[
        DataRequired(),
        Length(min=10, max=20)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    submit = SubmitField('Login')

class AdminLoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8)
    ])
    submit = SubmitField('Login')

class RestaurantForm(FlaskForm):
    restaurant_name = StringField('Restaurant Name', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    email = StringField('Email Address', validators=[
        DataRequired(),
        Email()
    ])
    contact_person = StringField('Contact Person', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    phone_number = StringField('Phone Number', validators=[
        DataRequired(),
        Length(min=10, max=20)
    ])
    website_url = StringField('Website URL', validators=[
        Optional(),
        URL()
    ])
    website_username = StringField('Website Username', validators=[
        Optional(),
        Length(max=100)
    ])
    website_password = StringField('Website Password', validators=[
        Optional(),
        Length(max=100)
    ])
    submit = SubmitField('Save Restaurant') 