from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, PasswordField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class DelegateOrdersToDriver(FlaskForm):
    driver = SelectField('Delivery Driver', coerce=str, validate_choice=False, validators=[DataRequired()])
    submitDelegateOrdersToDriver = SubmitField('Delegate')