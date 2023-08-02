from app import app, connect

from flask import render_template, request, redirect, url_for, session, flash
import re
import mysql.connector

import os
import bcrypt

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn
                
app.secret_key = 'youCannotGuessIt'

# check whether a user is admin or staff or customer
def userInfo():
    connection = getCursor()
    connection.execute('SELECT userID, userPermission, userName FROM users \
                           WHERE userID = %s;', (session['id'],))
    userBasic = connection.fetchall()

    if userBasic[0][1] == 1 or userBasic[0][1] == 2:
        infoTable = 'staffinfo'
    else:
        infoTable = 'customerinfo'
    
    getInfoDetails = f'SELECT userID, realName, email, phoneNumber, userAddress FROM {infoTable} WHERE userID = %s;'
    connection.execute(getInfoDetails, (session['id'],))
    userInfoDetails = connection.fetchall()
    return userBasic, userInfoDetails

# encapsulate the passwordEncrypt function
def passwordEncrypt(userPassword):
    bytes = userPassword.encode('utf-8')
    salt = bcrypt.gensalt()
    hashedPsw = bcrypt.hashpw(bytes, salt)
    return hashedPsw


# car list showing all car information
@app.route("/carsList")
def carsList():
    if 'loggedin' in session:
        connection = getCursor()
        connection.execute('SELECT * FROM cars;')
        allCars = connection.fetchall()
        return render_template('carList.html', allCars=allCars)

    else:
        return redirect('/')

# car list but editable in order to add/edit
@app.route("/carsListEdit", methods = ['GET','POST'])
def carsListEdit():
    if 'loggedin' in session and userInfo()[0][0][1] != 3:
        connection = getCursor()
        connection.execute('SELECT * FROM cars;')
        allCars = connection.fetchall()
        return render_template('carListEdit.html', allCars=allCars)


    else:
        return redirect('/')
    
# car  add/edit
@app.route("/carsOperation", methods = ['POST'])
def carsOperation():

    rego = request.form.get('rego')
    year = request.form.get('year')
    brand = request.form.get('brand')
    model = request.form.get('model')
    seat = request.form.get('seat')
    price = request.form.get('price')
    carID = request.form.get('carID')
    action = request.form.get('action')

    #permission confirm
    if 'loggedin' in session and userInfo()[0][0][1] != 3:
        if action != 'delete':
            # Update car informations, including photo
            connection = getCursor()
            connection.execute('UPDATE cars \
                                SET rego=%s, brand=%s, model=%s, yearBuild=%s, seat=%s, price=%s \
                                WHERE carID = %s;', \
                                (rego, brand, model, year, seat, price, carID))
            
            if 'carfile' in request.files and request.files['carfile'].filename != '':
                carfile = request.files['carfile']
                carID = request.form.get('carID')
                filename = f"{carID}.jpg"
                filepath = os.path.join('app','static', 'img', 'cars', filename)
                carfile.save(filepath)
            
            flash('Car edited!', 'success')
            return redirect('/carsListEdit')
        else:
            # Delete car informations, including photo
            connection = getCursor()
            connection.execute('DELETE FROM cars WHERE carID = %s;',(carID,))

            filename = f"{carID}.jpg"
            filepath = os.path.join('app', 'static', 'img', 'cars', filename)
            try:
                os.remove(filepath)
            except FileNotFoundError:
                pass
            flash('Car deleted!', 'success')
            return redirect('/carsListEdit')

    else:
        return redirect('/')
    
# add a new car
@app.route("/carsAdd", methods = ['POST'])
def carsAdd():
    rego = request.form.get('regoAdd')
    year = request.form.get('yearAdd')
    brand = request.form.get('brandAdd')
    model = request.form.get('modelAdd')
    seat = request.form.get('seatAdd')
    price = request.form.get('priceAdd')

    #permission confirm
    if 'loggedin' in session and userInfo()[0][0][1] != 3:
        connection = getCursor()
        connection.execute('INSERT INTO cars \
                            (rego, brand, model, yearBuild, seat, price) \
                            VALUES (%s, %s, %s, %s, %s, %s);', \
                                (rego, brand, model, year, seat, price))
        
        if 'carfileAdd' in request.files and request.files['carfileAdd'].filename != '':
            carfile = request.files['carfileAdd']
            connection.execute('SELECT * FROM cars WHERE carID = (SELECT MAX(carID) FROM cars);')
            carID = connection.fetchall()[0][0]
            # carID = request.form.get('carID')
            filename = f"{carID}.jpg"
            filepath = os.path.join('app','static', 'img', 'cars', filename)
            carfile.save(filepath)
        
        flash('New car created!', 'success')
        return redirect('/carsListEdit')


    else:
        return redirect('/')
    
#Manage customers

@app.route("/customers", methods = ['GET', 'POST'])
def customers():
    
    userName = request.form.get('userName')
    userPassword = request.form.get('userPassword')
    email = request.form.get('userEmail')
    phoneNumber = request.form.get('phoneNumber')
    userAddress = request.form.get('userAddress')
    realName = request.form.get('realName')

    userIDExisting = request.form.get('userIDExisting')
    userPasswordExisting = request.form.get('userPasswordExisting')
    emailExisting = request.form.get('userEmailExisting')
    phoneNumberExisting = request.form.get('phoneNumberExisting')
    userAddressExisting = request.form.get('userAddressExisting')
    realNameExisting = request.form.get('realNameExisting')
    userInfoListExisting = [realNameExisting,  emailExisting, phoneNumberExisting, userAddressExisting]
    infoTableExisting = ['realName', 'email', 'phoneNumber', 'userAddress']

    action = request.form.get('action')
    
    #Add new customers
    if userName:
        #form info back-end validation
        connection = getCursor()
        connection.execute('SELECT * FROM users WHERE userName = %s', (userName,))
        account = connection.fetchall()
        # If account exists show error and validation checks
        if account:
            flash('Failed sign up: Account already exists!', 'success')
            return redirect('/customers')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Failed sign up: Invalid email address!', 'success')
            return redirect('/customers')

        else:
        # use bcrypt to encrypt the password
            encryptedPassword = passwordEncrypt(userPassword)
            # create account in users
            connection.execute("INSERT INTO users \
                            (userPermission,userName,userPassword) \
                            VALUES (3, %s, %s);", \
                                (userName, encryptedPassword))
            
            # create account in customers
            connection.execute('SELECT userID FROM users WHERE userName = %s', (userName,))
            userID = connection.fetchall()[0][0]

            connection.execute("INSERT INTO customerinfo \
                            (userID, realName, \
                            email, phoneNumber, userAddress)\
                            VALUES (%s, %s, %s, %s, %s);", \
                                (userID, realName, \
                                email, phoneNumber, userAddress))
            
            flash('New account created!', 'success')
            return redirect('/customers')
    
    #Edit customers
    elif userIDExisting and action != 'delete':
        #update info
        
        if emailExisting or phoneNumberExisting or userAddressExisting or realNameExisting:
            for index, item in enumerate(userInfoListExisting):
                if item:
                    updateCustomerInfo = f'UPDATE customerinfo SET {str(infoTableExisting[index])} = "{item}" WHERE userID = %s ;'
                    connection = getCursor()
                    connection.execute(updateCustomerInfo,\
                                        (userIDExisting,))

        if userPasswordExisting:
            connection = getCursor()
            connection.execute('UPDATE users SET userPassword = %s WHERE userID = %s ;', (passwordEncrypt(userPassword), userIDExisting,))

        
        flash('Customer profile update successful!', 'success')
        return redirect('/customers')
    
    #Delete customer
    elif userIDExisting and action == 'delete':
        connection = getCursor()
        connection.execute('DELETE FROM users WHERE userID = %s;',(userIDExisting,))
        flash('Customer removed!', 'success')
        return redirect('/customers')

    
    
    elif 'loggedin' in session and userInfo()[0][0][1] != 3:
        connection = getCursor()
        connection.execute('SELECT * FROM users JOIN customerinfo ON users.userID=customerinfo.userID;')
        customerInfo = connection.fetchall()

        userPermissionJinja = userInfo()[0][0][1]
        return render_template('customers.html', customerInfo=customerInfo, userInfoJinja=userPermissionJinja)
    else:
        return redirect('/')
    
# manage staff, basically the same function as managing customers
@app.route("/staff", methods = ['GET', 'POST'])
def staff():
    
    userName = request.form.get('userName')
    userPassword = request.form.get('userPassword')
    email = request.form.get('userEmail')
    phoneNumber = request.form.get('phoneNumber')
    userAddress = request.form.get('userAddress')
    realName = request.form.get('realName')

    userIDExisting = request.form.get('userIDExisting')
    userPasswordExisting = request.form.get('userPasswordExisting')
    emailExisting = request.form.get('userEmailExisting')
    phoneNumberExisting = request.form.get('phoneNumberExisting')
    userAddressExisting = request.form.get('userAddressExisting')
    realNameExisting = request.form.get('realNameExisting')
    userInfoListExisting = [realNameExisting,  emailExisting, phoneNumberExisting, userAddressExisting]
    infoTableExisting = ['realName', 'email', 'phoneNumber', 'userAddress']

    action = request.form.get('action')
    
    #Add new customers
    if userName:
        #form info back-end validation
        connection = getCursor()
        connection.execute('SELECT * FROM users WHERE userName = %s', (userName,))
        account = connection.fetchall()
        # If account exists show error and validation checks
        if account:
            flash('Failed sign up: Account already exists!', 'success')
            return redirect('/staff')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Failed sign up: Invalid email address!', 'success')
            return redirect('/staff')

        else:
        # use bcrypt to encrypt the password
            encryptedPassword = passwordEncrypt(userPassword)
            # create account in users
            connection.execute("INSERT INTO users \
                            (userPermission,userName,userPassword) \
                            VALUES (3, %s, %s);", \
                                (userName, encryptedPassword))
            
            # create account in staff
            connection.execute('SELECT userID FROM users WHERE userName = %s', (userName,))
            userID = connection.fetchall()[0][0]

            connection.execute("INSERT INTO staffinfo \
                            (userID, realName, \
                            email, phoneNumber, userAddress)\
                            VALUES (%s, %s, %s, %s, %s);", \
                                (userID, realName, \
                                email, phoneNumber, userAddress))
            
            flash('New staff account created!', 'success')
            return redirect('/staff')
    
    #Edit customers
    elif userIDExisting and action != 'delete':
        #update info
        
        if emailExisting or phoneNumberExisting or userAddressExisting or realNameExisting:
            for index, item in enumerate(userInfoListExisting):
                if item:
                    updateStaffInfo = f'UPDATE staffinfo SET {str(infoTableExisting[index])} = "{item}" WHERE userID = %s ;'
                    connection = getCursor()
                    connection.execute(updateStaffInfo,\
                                        (userIDExisting,))

        if userPasswordExisting:
            connection = getCursor()
            connection.execute('UPDATE users SET userPassword = %s WHERE userID = %s ;', (passwordEncrypt(userPassword), userIDExisting,))
        
        flash('Staff profile update successful!', 'success')
        return redirect('/staff')
    
    #Delete customer
    elif userIDExisting and action == 'delete':
        connection = getCursor()
        connection.execute('DELETE FROM users WHERE userID = %s;',(userIDExisting,))
        flash('Staff removed!', 'success')
        return redirect('/staff')

    
    
    elif 'loggedin' in session and userInfo()[0][0][1] == 1:
        connection = getCursor()
        connection.execute('SELECT * FROM users JOIN staffinfo ON users.userID=staffinfo.userID;')
        staffInfo = connection.fetchall()

        return render_template('staff.html', staffInfo=staffInfo)
    else:
        return redirect('/')