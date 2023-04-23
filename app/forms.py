from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, EqualTo

class LogIn(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()

class SignUpForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField()

class Address(FlaskForm):

    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip = IntegerField('zip', validators=[DataRequired()])

class Inventory(FlaskForm):

    product_name = StringField('Product Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    description = IntegerField('Description', validators=[DataRequired()])
    image = StringField('Product Name', validators=[DataRequired()])
    image2 = StringField('Product Name', validators=[DataRequired()])
    image3 = StringField('Product Name', validators=[DataRequired()])
    image4 = StringField('Product Name', validators=[DataRequired()])