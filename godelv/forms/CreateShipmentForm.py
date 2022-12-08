from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, PasswordField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class AddressInformationForm(FlaskForm):
    # here f prefix means from, r means receiver
    fname = StringField('Your Name', validators=[DataRequired(), Length(min=2, max=200)])
    faddress = StringField('Address', validators=[DataRequired(), Length(min=2, max=200)])
    fapartment = StringField('Apartment', validators=[DataRequired(), Length(min=2, max=200)])
    fzip = StringField('ZIP', validators=[DataRequired(), Length(min=5, max=6)])  # only accepting US zip code
    fcity = StringField('City', validators=[DataRequired(), Length(min=2, max=200)])
    fstate = StringField('State', validators=[DataRequired(), Length(min=2, max=200)])
    fmobileNo = StringField('Mobile', validators=[DataRequired(), Length(min=10, max=10), Regexp(regex='^[0-9]{10}$')])
    femail = StringField('Email', validators=[DataRequired(), Email()])

    rname = StringField('Recipient Name', validators=[DataRequired(), Length(min=2, max=200)])
    raddress = StringField('Address', validators=[DataRequired(), Length(min=2, max=200)])
    rapartment = StringField('Apartment', validators=[DataRequired(), Length(min=2, max=200)])
    rzip = StringField('ZIP', validators=[DataRequired(), Length(min=5, max=6)])  # only accepting US zip code
    rcity = StringField('City', validators=[DataRequired(), Length(min=2, max=200)])
    rstate = StringField('State', validators=[DataRequired(), Length(min=2, max=200)])
    rmobileNo = StringField('Mobile', validators=[DataRequired(), Length(min=10, max=10), Regexp(regex='^[0-9]{10}$')])
    remail = StringField('Email', validators=[DataRequired(), Email()])

    submit1 = SubmitField('Continue')


class ShippingDetailsForm(FlaskForm):
    carriername = SelectField('Carrier', coerce=str, validate_choice=False, validators=[DataRequired()])
    servicename = SelectField('Service', coerce=str, validate_choice=False, validators=[DataRequired()])
    packageweight = FloatField('Package Weight', validators=[DataRequired()])
    packagesize = SelectField('Package Size Category', coerce=str, validate_choice=False, validators=[DataRequired()])
    # packagetimeOpts = SelectField('Expected Delivery Within', coerce=str, validate_choice=False, validators=[DataRequired()])
    submit2 = SubmitField('Continue')
