from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class RegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    dateOfBirth = DateField('Date of Birth', validators=[DataRequired()])
    mobileNo = StringField('Mobile', validators=[DataRequired(), Length(min=10, max=10), Regexp(regex='^[0-9]{10}$')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=10)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    userType = SelectField('Role', validators=[DataRequired()], choices=[('CUSTOMER', 'Customer'), ('ADMINISTRATOR', 'Carrier Admin'),
                                                                         ('DELIVERYDRIVER', 'Carrier Delivery Driver')
                                                                         ])
    carrierName = SelectField('Carrier Name', coerce=str, validate_choice=False)
    managerID = SelectField('Carrier Manager', coerce=str, validate_choice=False)
    submitRegistration = SubmitField('Sign Up')
