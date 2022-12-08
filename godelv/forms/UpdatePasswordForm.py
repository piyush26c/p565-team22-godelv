from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class UpdatePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=10)])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')
