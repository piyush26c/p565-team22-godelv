from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, PasswordField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class TrackbyIDForm(FlaskForm):
    trackingID = StringField('Tracking ID', validators=[DataRequired(), Length(min=17, max=50)])
    submitTrackingID = SubmitField('Submit')
