from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, PasswordField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class AddServiceForm(FlaskForm):
    servicename = StringField('Service Name', validators=[DataRequired(), Length(min=5, max=500)])
    dimension = SelectField('Dimension', validators=[DataRequired()], choices=[('Small', 'Small'), ('Medium', 'Medium'),
                                                                         ('Large', 'Large')
                                                                         ], validate_choice=False)
    price = DecimalField('Price (per lb)', validators=[DataRequired()])
    addService = SubmitField('Add')
