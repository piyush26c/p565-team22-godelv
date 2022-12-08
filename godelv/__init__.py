from flask import Flask
from godelv.forms.RegistrationForm import RegistrationForm
from godelv.forms.LoginForm import LoginForm
from flask_bcrypt import Bcrypt
import pymysql
from flask_mail import Mail


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = '7981c387e281b6f0bc719f5259a2b2cd'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'godelvcompany@gmail.com'
app.config['MAIL_PASSWORD'] = 'msjqfmlznsqqrevq'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:piyush1234@localhost/godelv'

mail = Mail(app)

# connection = pymysql.connect(host="localhost", port=3306, user="root", passwd="piyush1234", db="godelv",cursorclass = pymysql.cursors.DictCursor)
# #Creating a connection cursor
# cursor = connection.cursor()
from godelv import routes
