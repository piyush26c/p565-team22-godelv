from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class LoginForm(FlaskForm):
    id = StringField('Username / Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=10)])
    otp = StringField('OTP-2FA', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Login')
