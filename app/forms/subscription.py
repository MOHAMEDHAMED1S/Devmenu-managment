from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, URL

class SubscriptionForm(FlaskForm):
    restaurant_name = StringField('Restaurant Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    website_url = StringField('Website URL', validators=[Optional(), URL()])
    website_username = StringField('Website Username', validators=[Optional()])
    website_password = StringField('Website Password', validators=[Optional()])
    subscription_price = FloatField('Subscription Price', validators=[DataRequired()])
    subscription_term = SelectField('Subscription Term', 
                                  choices=[('monthly', 'Monthly'), 
                                          ('quarterly', 'Quarterly'), 
                                          ('yearly', 'Yearly')],
                                  validators=[DataRequired()])
    payment_method = SelectField('Payment Method',
                                choices=[('vodafone_cash', 'Vodafone Cash'),
                                         ('orange_cash', 'Orange Cash'),
                                        ('insta_pay', 'Insta Pay'),
                                        ('cash', 'Cash'),
                                        ('bank_transfer', 'Bank Transfer'),
                                        ('paypal', 'PayPal')],
                                validators=[DataRequired()])
    submit = SubmitField('Save Subscription') 