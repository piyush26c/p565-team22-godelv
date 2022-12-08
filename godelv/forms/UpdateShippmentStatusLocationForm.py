from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, PasswordField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

class UpdateShippmentStatusLocationForm(FlaskForm):
    option = SelectField('Update Location / Status', choices=[('STATUS', 'Status'), ('LOCATION', 'Location')])
    status = SelectField('Status', choices=[('ON THE WAY', 'ON THE WAY'), ('DELIVERED', 'DELIVERED')] )
    address = StringField('Address', validators=[ Length(min=2, max=200)])
    zip = StringField('ZIP', validators=[Length(min=5, max=6)])  # only accepting US zip code
    city = StringField('City', validators=[Length(min=2, max=200)])
    state = StringField('State', validators=[Length(min=2, max=200)])
    submitUpdateShippmentStatusLocationForm = SubmitField('Submit')