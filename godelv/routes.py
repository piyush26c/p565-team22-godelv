import pyqrcode

from godelv.forms.RegistrationForm import RegistrationForm
from godelv.forms.LoginForm import LoginForm
from godelv.forms.PasswordResetForm import PasswordResetForm
from godelv.forms.UpdatePasswordForm import UpdatePasswordForm
from godelv.forms.CreateShipmentForm import AddressInformationForm, ShippingDetailsForm
from godelv.forms.TrackbyIDForm import TrackbyIDForm
from godelv.forms.AddServiceForm import AddServiceForm
from godelv.forms.DelegateOrdersToDriver import DelegateOrdersToDriver
from godelv.forms.UpdateShippmentStatusLocationForm import UpdateShippmentStatusLocationForm
from flask import Flask, render_template, url_for, flash, redirect, session, abort, request, make_response, jsonify
# from godelv import app, connection, cursor, bcrypt, mail
from godelv import app, bcrypt, mail
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Message

import folium
from geopy import Nominatim

import os
import base64
from io import BytesIO
import onetimepass
import pymysql


def dbconnect():
    # return pymysql.connect(host="localhost", port=3306, user="root", passwd="piyush1234", db="godelv",
    #                              cursorclass=pymysql.cursors.DictCursor)
    return pymysql.connect(host="sql9.freesqldatabase.com", port=3306, user="sql9583519", passwd="v2qff4bvAd",
                           db="sql9583519",
                           cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
@app.route('/home')
def home():  # put application's code here
    return render_template('home.html')


def generateUsername(firstName_, lastName_, dob):
    op = firstName_ + lastName_[0] + str(dob.year)
    return op


def get_totp_uri(email_, otp_secret_):
    return 'otpauth://totp/GoDelv-2FA:{0}?secret={1}&issuer=2FA-Demo'.format(email_, otp_secret_)


def verify_totp(token_, otp_secret_):
    return onetimepass.valid_totp(token_, otp_secret_)


@app.route('/twofactor')
def two_factor_setup():
    if 'userType' not in session:
        return redirect(url_for('home'))

    # if user is None:
    #     return redirect(url_for('index'))

    # since this page contains the sensitive qrcode, make sure the browser
    # does not cache it
    print('two_factor_authentication')
    return render_template('two_factor_setup.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route('/qrcode')
def qrcode():
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()
    if 'userType' not in session:
        return redirect(url_for('home'))

    # if user is None:
    #     abort(404)

    # render qrcode for FreeTOTP
    cursor.execute('SELECT otpSecret FROM Login WHERE email = % s', (session['useremail']))
    otp_secret = cursor.fetchone()['otpSecret']
    url = pyqrcode.create(get_totp_uri(session['useremail'], otp_secret))
    stream = BytesIO()
    url.svg(stream, scale=5)

    # for added security, remove username from session
    del session['userType']
    del session['useremail']
    cursor.close()
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route('/fetchdropdowndata_carriers', methods=['GET', 'POST'])
def fetchdropdowndata_carriers():
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()
    if request.method == "POST":
        cursor.execute('SELECT *  FROM Carrier')
        carriers = cursor.fetchall()
        jsonOutput = []
        if carriers:
            for aCarrier in carriers:
                jsonOutput.append({"value": aCarrier["carrierID"], "display": aCarrier["carrierName"]})
        else:
            print('console:- no carriers found')
    cursor.close()
    return jsonify(jsonOutput)


@app.route('/register', methods=['GET', 'POST'])
def register():
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()
    form = RegistrationForm()
    form.carrierName.choices = []
    form.managerID.choices = []

    if form.submitRegistration.data and form.validate():
        print(form.userType.data, form.carrierName.data)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        userName = generateUsername(form.firstName.data, form.lastName.data, form.dateOfBirth.data)
        otpSecret = base64.b32encode(os.urandom(10)).decode('utf-8')
        if form.userType.data == 'CUSTOMER':
            cursor.execute('INSERT INTO Customer VALUES(% s, % s, % s, % s, % s)',
                           (form.email.data, form.firstName.data, form.lastName.data,
                            datetime.strftime(form.dateOfBirth.data, '%m/%d/%Y'),
                            form.mobileNo.data))
            cursor.execute('INSERT INTO Login VALUES(% s, % s, % s, % s, % s)',
                           (form.email.data, userName, hashed_password, 'CUSTOMER', otpSecret))

        elif form.userType.data == 'ADMINISTRATOR':
            cursor.execute('INSERT INTO Administrator VALUES(% s, % s, % s, % s, % s, % s)',
                           (form.email.data, form.firstName.data, form.lastName.data,
                            datetime.strftime(form.dateOfBirth.data, '%m/%d/%Y'),
                            form.mobileNo.data, form.carrierName.data))
            cursor.execute('INSERT INTO Login VALUES(% s, % s, % s, % s, % s)',
                           (form.email.data, userName, hashed_password, 'ADMINISTRATOR', otpSecret))
        else:
            # cursor.execute('SELECT carrierID FROM Carrier WHERE carrierName = % s', ())
            carrierID = form.carrierName.data
            print(form.email.data, form.managerID.data, form.firstName.data, form.lastName.data,
                  datetime.strftime(form.dateOfBirth.data, '%m/%d/%Y'),
                  form.mobileNo.data, str("FALSE"), carrierID)

            cursor.execute('INSERT INTO DeliveryDriver VALUES(% s, % s, % s, % s, % s, % s, % s, % s)',
                           (form.email.data, form.managerID.data, form.firstName.data, form.lastName.data,
                            datetime.strftime(form.dateOfBirth.data, '%m/%d/%Y'),
                            form.mobileNo.data, str("FALSE"), carrierID))
            cursor.execute('INSERT INTO Login VALUES(% s, % s, % s, % s, % s)',
                           (form.email.data, userName, hashed_password, 'DELIVERYDRIVER', otpSecret))

        connection.commit()
        flash(f'Account created sucessfully!, Here is your username: {userName}', 'success')
        session['useremail'] = form.email.data
        session['userType'] = form.userType.data
        return redirect(url_for('two_factor_setup'))

        return render_template('display_username.html', userName=userName)
    else:
        print(form.errors)
    cursor.close()
    return render_template('register.html', page_title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()
    form = LoginForm()
    if form.validate_on_submit():
        cursor.execute('SELECT * FROM Login where email = % s or username = % s', (form.id.data, form.id.data))
        userDBData = cursor.fetchone()

        if userDBData and bcrypt.check_password_hash(userDBData['password'],
                                                     form.password.data) and verify_totp(form.otp.data,
                                                                                         userDBData[
                                                                                             'otpSecret']):
            flash('You have been logged in!', 'success')
            session['useremail'] = userDBData['email']
            session['userType'] = userDBData['userType']
            session['username'] = userDBData['username']

            if session['userType'] == 'CUSTOMER':
                return redirect(url_for('customerhome'))
            elif session['userType'] == 'ADMINISTRATOR':
                cursor.execute(
                    "SELECT carrierName FROM Carrier WHERE carrierID = (SELECT carrierID FROM Administrator where email = % s)",
                    (session['useremail']))
                session['carrierName'] = cursor.fetchone()['carrierName']
                return redirect(url_for('adminhome'))
            else:
                cursor.execute(
                    "SELECT carrierName FROM Carrier WHERE carrierID = (SELECT carrierID FROM DeliveryDriver where email = % s)",
                    (session['useremail']))
                session['carrierName'] = cursor.fetchone()['carrierName']
                return redirect(url_for('deliverydriverhome'))
        else:
            flash('Login Unsuccessful. Please check username, password or otp!', 'danger')
            return redirect(url_for('login'))
    cursor.close()
    return render_template('login.html', page_title='Login', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))


def get_token(expiresInSeconds, email_):
    serial = Serializer(app.config['SECRET_KEY'],
                        expires_in=expiresInSeconds)  # expires takes input in seconds, 900 seconds means 15mins
    token = serial.dumps({'email': email_}).decode('utf-8')
    return token


def verify_token(tokenString):
    serial = Serializer(app.config['SECRET_KEY'])
    userEmail = serial.loads(tokenString)['email']
    if userEmail != None:
        return [True, userEmail]
    return [False]


def send_email(email_):
    token = get_token(900, email_)
    emailmsg = Message('GoDelv Account Password Reset Request', recipients=[email_], sender='godelvcompany@gmail.com')
    emailmsg.body = f'''
    Hi,
    GoDelv received a requrest to reset the password for this account.Click the button below to reset your password. 
    The link below will take you to a secure page where you can change your password.
    {url_for('reset_token', token=token, _external=True)}
    
    
    
    If you don't want to reset your password, please ignore this message. Your password will not be reset. 
    '''
    mail.send(emailmsg)


@app.route('/passworreset', methods=['GET', 'POST'])
def passwordReset():
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()
    # passwordReset is done only for userType: CUSTOMER
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = cursor.execute('SELECT * FROM Login WHERE email = % s', (form.email.data))
        if user:
            send_email(form.email.data)
            flash('Password reset email set. Kindly check your mailbox', 'success')
        else:
            flash('Account does not exists.', 'danger')
    cursor.close()
    return render_template('password_reset.html', legend='Password Reset', form=form)


@app.route('/passworreset/<token>', methods=['GET', 'POST'])
def reset_token(token):
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()
    op = verify_token(token)
    if op[0] == False:
        flash('That is invalid token or expired! Please try again.', 'warning')
        return redirect(url_for('login'))

    form = UpdatePasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        cursor.execute('UPDATE Login SET password = % s WHERE email = % s', (hashed_password, op[1]))
        connection.commit()

        flash('Password changed successfully! Please Login!', 'success')
        return redirect(url_for('login'))
    cursor.close()
    return render_template('update_password.html', legend='Password Reset', form=form)


@app.route('/customerhome', methods=['GET', 'POST'])
def customerhome():
    return render_template('customer_home.html')


@app.route('/adminhome', methods=['GET', 'POST'])
def adminhome():
    return render_template('adminhome.html')


@app.route('/delegateordertodriver/<string:SID>', methods=['GET', 'POST'])
def delegateordertodriver(SID):
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()
    delegateordertodriverForm = DelegateOrdersToDriver()
    print('delegateorderstodriver(): ', SID, type(SID))
    if request.method == "GET":

        drivers = []
        cursor.execute('SELECT * FROM DeliveryDriver WHERE isEngage = "FALSE"')
        rows = cursor.fetchall()
        for row in rows:
            drivers.append((row['email'], row['firstName'] + " " + row['lastName'] + "(" + row['email'] + ")"))
        print(drivers)
        delegateordertodriverForm.driver.choices = drivers
        cursor.close()
        return render_template('assigndriverfororder.html', delegateordertodriverForm=delegateordertodriverForm,
                               shippingID=SID)
    else:
        cursor.execute('UPDATE Shippment SET deliveryDriverID = % s WHERE SID = % s',
                       (delegateordertodriverForm.driver.data, SID))
        connection.commit()
        cursor.execute('UPDATE DeliveryDriver SET isEngage = "TRUE" WHERE email = % s',
                       (delegateordertodriverForm.driver.data))
        connection.commit()
        cursor.execute('UPDATE Tracking SET deliveryStatus = "PICKED BY CARRIER" WHERE TID = %s', (SID))
        connection.commit()

        print('updation of deliverydriverid in shipment successful', delegateordertodriverForm.driver.data)
        cursor.close()
        flash('Delivery Driver Assigned Successfully!', 'success')
        return redirect(url_for('delegateorders'))
    cursor.close()
    return render_template()


@app.route('/delegateorders', methods=['GET', 'POST'])
def delegateorders():
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()
    if request.method == "GET":
        cursor.execute(
            "SELECT * FROM Shippment WHERE carrierName = % s AND deliveryDriverID = '' AND SID in (SELECT TID FROM Tracking WHERE deliveryStatus = 'ORDER CONFIRMED')",
            (session['carrierName']))
        rows = cursor.fetchall()
        tablerows = []

        for row in rows:
            tablerows.append(
                {"SID": row['SID'], "raddress": row['raddress'], "rcity": row['rcity'], "rstate": row['rstate'],
                 "rzip": row['rzip']})
        print('delegateorders(): ', tablerows)
        cursor.close()
        return render_template('delegateorders.html', tablerows=tablerows)


@app.route('/updateShippmentDeliveryDriver', methods=['GET'])
def updateShippmentDeliveryDriver():
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()
    cursor.execute(
        'SELECT * FROM Tracking WHERE deliveryStatus != "DELIVERED" AND deliveryStatus != "PICKED BY CARRIER"')
    rows = cursor.fetchall()
    tablerows = []

    for row in rows:
        tablerows.append({"SID": row['TID'], "Delivery Status": row['deliveryStatus']})
    print("updateShippmentStatusDeliveryDriver(): ", tablerows)
    cursor.close()
    return render_template("updateShippmentLocation.html", tablerows=tablerows)


@app.route('/updateShippmentStatusLocationDeliveryDriver/<string:SID>', methods=['GET', 'POST'])
def updateShippmentStatusLocationDeliveryDriver(SID):
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()
    updtShippmentStatusLocationform = UpdateShippmentStatusLocationForm()
    print(updtShippmentStatusLocationform.errors,
          updtShippmentStatusLocationform.submitUpdateShippmentStatusLocationForm.data,
          updtShippmentStatusLocationform.status.data)
    if updtShippmentStatusLocationform.submitUpdateShippmentStatusLocationForm.data:

        if updtShippmentStatusLocationform.option.data == "STATUS":
            cursor.execute('UPDATE Tracking SET deliveryStatus = % s WHERE TID = % s',
                           (updtShippmentStatusLocationform.status.data, SID))
            connection.commit()
            if updtShippmentStatusLocationform.status.data == "DELIVERED":
                cursor.execute('SELECT * FROM Shippment WHERE SID = % s', SID)
                shippmentRow = cursor.fetchone()

                emailsubjectR = shippmentRow['rname'] + ", Your package has arrived!"
                emailmsgR = Message(emailsubjectR, recipients=[shippmentRow['remail']],
                                    sender='godelvcompany@gmail.com')

                emailsubjectS = shippmentRow['fname'] + ", Your package is delivered!"
                emailmsgS = Message(emailsubjectS, recipients=[shippmentRow['femail']],
                                    sender='godelvcompany@gmail.com')

                emailmsgR.body = f'''
                Dear customer,
                We are happy to inform you that GoDelv had successfully delivered the shipment at respective given address.
                Shipment ID: {shippmentRow['SID']}
                Carrier: {shippmentRow['carrierName']}
                Delivery Address: 
                {shippmentRow['rname']}
                {shippmentRow['raddress']}
                Apartment {shippmentRow['rapartment']}
                {shippmentRow['rcity']}, {shippmentRow['rstate']} {shippmentRow['rzip']}
                USA
                
                
                Thank you for availing services from GoDelv company. For any further queries, kindly write us at godelvcompany@gmail.com
 
                '''
                emailmsgS.body = emailmsgR.body
                mail.send(emailmsgR)
                mail.send(emailmsgS)

        else:
            cursor.execute('UPDATE Tracking SET address = % s, zip = % s, city = % s, state = % s WHERE TID = % s', (
                updtShippmentStatusLocationform.address.data, updtShippmentStatusLocationform.zip.data,
                updtShippmentStatusLocationform.city.data, updtShippmentStatusLocationform.state.data, SID))
            connection.commit()
        flash("Updation done successfully!", 'success')
        return redirect(url_for('updateShippmentDeliveryDriver'))
    cursor.close()
    return render_template('updateShippmentStatusLocation.html',
                           updtShippmentStatusLocationform=updtShippmentStatusLocationform)


@app.route('/deliverydriverhome', methods=['GET', 'POST'])
def deliverydriverhome():
    return render_template('deliverydriver_home.html')


@app.route('/fetchdropdowndata_carriername', methods=['POST'])
def fetchdropdowndata_carriername():
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()
    if request.method == "POST":
        carriername = request.form['carriername']
        print(carriername)
        cursor.execute("SELECT deliveryServiceName FROM DeliveryService  WHERE carrierName = % s", (carriername))
        deliveryServices = cursor.fetchall()
        jsonOutput = []
        print(deliveryServices)
        for row in deliveryServices:
            jsonOutput.append({"value": row['deliveryServiceName'], "display": row['deliveryServiceName']})
    cursor.close()
    return jsonify(jsonOutput)


@app.route('/fetchdropdowndata_carriermanagers', methods=['POST'])
def fetchdropdowndata_carriermanagers():
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()
    if request.method == "POST":
        carrierid = request.form['carriername']
        print('thisisfetchdropdowndata_carriermanagers: ', carrierid)

        cursor.execute("SELECT firstName, lastName, email FROM Administrator  WHERE carrierID = % s", (carrierid))
        deliveryManagers = cursor.fetchall()
        jsonOutput = []
        print('managers', deliveryManagers)
        for row in deliveryManagers:
            jsonOutput.append({"value": row['email'],
                               "display": row['firstName'] + " " + row['lastName'] + " (" + row['email'] + ")"})
    cursor.close()
    return jsonify(jsonOutput)


@app.route('/fetchdropdowndata_carrierdimensions', methods=['GET', 'POST'])
def fetchdropdowndata_carrierdimensions():
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()
    if request.method == "POST":
        carriername = request.form['carriername']
        print(carriername)
        cursor.execute("SELECT dimension FROM DeliveryService  WHERE carrierName = % s", (carriername))
        dimensions = cursor.fetchall()
        jsonOutput = []
        print(dimensions)
        for row in dimensions:
            jsonOutput.append({"value": row['dimension'], "display": row['dimension']})
    cursor.close()
    return jsonify(jsonOutput)


@app.route('/insertShippmentIDDB', methods=['POST'])
def insertShippmentIDDB():
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()

    if request.method == "POST":
        jsonOutput = []
        trackingid = request.form['trackingid']
        jsonOutput.append({'trackingid': trackingid})

        print('insertShippmentIDDB(): trackingid', trackingid)

        print(str(trackingid), session['shippment_fname'], session['shippment_faddress'],
              session['shippment_fapartment'],
              session['shippment_fzip'], session['shippment_fcity'], session['shippment_fstate'],
              session['shippment_fmobileNo'],
              session['shippment_femail'], session['shippment_rname'], session['shippment_raddress'],
              session['shippment_rapartment'],
              session['shippment_rzip'], session['shippment_rcity'], session['shippment_rstate'],
              session['shippment_rmobileNo'],
              session['shippment_remail'], session['shippment_carrierName'], session['shippment_deliveryServiceName'],
              session['shippment_dimension'],
              session['shippment_price'], session['shippment_weight'], session['shippment_deliveryDriverID'],
              session['shippment_customerID']
              )

        # inserting data into shippment and tracking table
        cursor.execute(
            'INSERT INTO Shippment VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (
                str(trackingid), session['shippment_fname'], session['shippment_faddress'],
                session['shippment_fapartment'],
                session['shippment_fzip'], session['shippment_fcity'], session['shippment_fstate'],
                session['shippment_fmobileNo'],
                session['shippment_femail'], session['shippment_rname'], session['shippment_raddress'],
                session['shippment_rapartment'],
                session['shippment_rzip'], session['shippment_rcity'], session['shippment_rstate'],
                session['shippment_rmobileNo'],
                session['shippment_remail'], session['shippment_carrierName'], session['shippment_deliveryServiceName'],
                session['shippment_dimension'],
                session['shippment_price'], session['shippment_weight'], session['shippment_deliveryDriverID'],
                session['shippment_customerID']
            ))
        connection.commit()

        cursor.execute('INSERT INTO Tracking VALUES(% s, % s, % s, % s, % s, % s, % s)',
                       (trackingid, "ORDER CONFIRMED", "", "", "", "", ""))
        connection.commit()

    cursor.close()
    return jsonify(jsonOutput)


@app.route('/createshipment', methods=['GET', 'POST'])
def createshipment():
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()
    addressInformationForm = AddressInformationForm()
    shippingDetailsForm = ShippingDetailsForm()
    carriername = []
    cursor.execute("SELECT carrierName FROM Carrier")
    temp_carriername = cursor.fetchall()
    print(temp_carriername)
    for row in temp_carriername:
        carriername.append((row['carrierName'], row['carrierName']))

    servicename = []
    packagesize = []

    shippingDetailsForm.carriername.choices = carriername
    shippingDetailsForm.packagesize.choices = packagesize
    shippingDetailsForm.servicename.choices = servicename

    if addressInformationForm.submit1.data and addressInformationForm.validate():
        flash("Address Details Verified Successfully!", 'success')
        session['shippment_fname'] = addressInformationForm.fname.data
        session['shippment_fapartment'] = addressInformationForm.fapartment.data
        session['shippment_faddress'] = addressInformationForm.faddress.data
        session['shippment_fzip'] = addressInformationForm.fzip.data
        session['shippment_fcity'] = addressInformationForm.fcity.data
        session['shippment_fstate'] = addressInformationForm.fstate.data
        session['shippment_fmobileNo'] = addressInformationForm.fmobileNo.data
        session['shippment_femail'] = addressInformationForm.femail.data

        session['shippment_rname'] = addressInformationForm.rname.data
        session['shippment_rapartment'] = addressInformationForm.rapartment.data
        session['shippment_raddress'] = addressInformationForm.faddress.data
        session['shippment_rzip'] = addressInformationForm.rzip.data
        session['shippment_rcity'] = addressInformationForm.rcity.data
        session['shippment_rstate'] = addressInformationForm.rstate.data
        session['shippment_rmobileNo'] = addressInformationForm.rmobileNo.data
        session['shippment_remail'] = addressInformationForm.remail.data
        print(addressInformationForm.errors)
    elif addressInformationForm.errors:
        flash("Error occured, Recheck the Address Details", "danger")
        return render_template('createshipment.html', addressInformationForm=addressInformationForm,
                               shippingDetailsForm=shippingDetailsForm)

    if shippingDetailsForm.submit2.data and shippingDetailsForm.validate():
        flash("Shipping Details Verified Successfully!", 'success')
        print('errors1:', request.form.keys(), request.form['servicename'], shippingDetailsForm.servicename.data)

        # inserting all shippment detials into session

        session['shippment_carrierName'] = shippingDetailsForm.carriername.data
        session['shippment_deliveryServiceName'] = shippingDetailsForm.servicename.data

        session['shippment_dimension'] = shippingDetailsForm.packagesize.data

        cursor.execute('SELECT price FROM DeliveryService WHERE deliveryServiceName = % s AND carrierName = % s',
                       (shippingDetailsForm.servicename.data, shippingDetailsForm.carriername.data))
        perlbprice = cursor.fetchone()['price']

        session['shippment_price'] = shippingDetailsForm.packageweight.data * perlbprice
        session['shippment_weight'] = shippingDetailsForm.packageweight.data

        session['shippment_deliveryDriverID'] = ""
        session['shippment_customerID'] = session['useremail']
        print(session)

    elif shippingDetailsForm.submit2.data and shippingDetailsForm.errors:
        print(shippingDetailsForm.errors)
        print(shippingDetailsForm.submit2.data)
        flash("Error occured, Recheck the Shipping Details", "danger")
        return render_template('createshipment.html', addressInformationForm=addressInformationForm,
                               shippingDetailsForm=shippingDetailsForm)
    cursor.close()
    return render_template('createshipment.html', addressInformationForm=addressInformationForm,
                           shippingDetailsForm=shippingDetailsForm)


@app.route('/trackbyid', methods=['GET', 'POST'])
def trackbyid():
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()
    trackbyIDForm = TrackbyIDForm()

    if request.method == 'POST':
        cursor.execute('SELECT * from Tracking WHERE TID = %s', (trackbyIDForm.trackingID.data))
        trackingDetails = cursor.fetchone()
        if trackingDetails:
            cursor.execute('SELECT * FROM Shippment WHERE SID = % s', (trackbyIDForm.trackingID.data))
            shippmentDetails = cursor.fetchone()

            if trackingDetails['deliveryStatus'] != "ORDER CONFIRMED":
                current_location = [trackingDetails['address'], trackingDetails['city'], trackingDetails['state'],
                                    trackingDetails['zip']]
                locator = Nominatim(user_agent="myGeocoder")
                current_location = locator.geocode(current_location[0])
                folium_map = folium.Map(location=(current_location.latitude, current_location.longitude), width='50%',
                                        height='50%', left='25%', zoom_start=14)
                folium.Marker(location=(current_location.latitude, current_location.longitude),
                              tooltip="Current Location").add_to(folium_map)

                folium_map.save('godelv/templates/map.html')

                cursor.close()
                return render_template('trackingbyidresult.html', trackbyIDForm=trackbyIDForm,
                                       trackingDetails=trackingDetails, shippmentDetails=shippmentDetails)
            else:
                return render_template('trackingbyidresult.html', trackbyIDForm=trackbyIDForm,
                                       trackingDetails=trackingDetails, shippmentDetails=shippmentDetails)


        else:
            flash('Invalid Tracking ID!', 'danger')

    cursor.close()
    return render_template('trackbyid.html', trackbyIDForm=trackbyIDForm)


@app.route('/addservice', methods=['GET', 'POST'])
def addservice():
    connection = dbconnect()
    # Creating a connection cursor
    cursor = connection.cursor()
    addserviceForm = AddServiceForm()

    if addserviceForm.validate_on_submit():
        cursor.execute("SELECT * FROM Carrier WHERE carrierName = % s", (session['carrierName']))
        carrierID = cursor.fetchone()['carrierID']
        cursor.execute("INSERT INTO DeliveryService VALUES(% s, % s, % s, % s, % s)", (
            addserviceForm.servicename.data, carrierID, session['carrierName'], addserviceForm.dimension.data,
            addserviceForm.price.data))
        connection.commit()
        flash("Services successfully added!", "success")
        return redirect(url_for('addservice'))

    cursor.close()
    return render_template('addservice.html', addserviceForm=addserviceForm)


@app.route('/searchandfilter', methods=['POST', 'GET'])
def searchandfilter():
    if request.method == 'POST':
        form_data = request.form
        print(form_data)
        print("\n kjfhliwhfiwjfiuhf")

        carrier = "carrierName LIKE \'%\' AND " if form_data['carrier'] == "viewall" else "carrierName = \'" + str(
            form_data['carrier']) + "\' AND "
        print(carrier)
        # weight="weights LIKE \'%\' AND " if form_data['weight'] == "viewall" else "weights=\'"+str(form_data['weight'])+"\' AND "

        shipping = "deliveryServiceName LIKE \'%\' " if form_data[
                                                            'shipping'] == "viewall" else "deliveryServiceName LIKE\'%" + str(
            form_data['shipping']) + "%\' "
        dimension = "AND dimension LIKE \'%\'" if form_data['dimension'] == "viewall" else "AND dimension=\'" + str(
            form_data['dimension']) + "\'"
        print(shipping, dimension)
        connection = dbconnect()
        # Creating a connection cursor
        cursor = connection.cursor()
        # conn = get_db_connection()
        sqlQueryString = "SELECT * FROM DeliveryService WHERE " + carrier + shipping + dimension
        print(sqlQueryString)
        cursor.execute(sqlQueryString)
        posts = cursor.fetchall()
        connection.close()



    else:
        # conn = get_db_connection()
        connection = dbconnect()
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM DeliveryService')
        posts = cursor.fetchall()
        connection.close()
    return render_template('searchandFilter.html', posts=posts)
