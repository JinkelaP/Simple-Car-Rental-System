from app import app, connect

from flask import render_template, request, redirect, url_for, session, flash
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
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
    connection.execute('SELECT userID, userPermission, email, phoneNumber, userAddress FROM users \
                           WHERE userID = %s', (session['id'],))
    userPermission = connection.fetchall()
    return userPermission

# encapsulate the passwordEncrypt function
def passwordEncrypt(userPassword):
    bytes = userPassword.encode('utf-8')
    salt = bcrypt.gensalt()
    hashedPsw = bcrypt.hashpw(bytes, salt)
    return hashedPsw

# redirect all 404 pages to my bootstrapped one.
@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html',session=session), 404

#The index page of the web app
@app.route("/", methods=['GET','POST'])
def index():    
    userName = request.form.get('userName')
    userPassword = request.form.get('userPassword')
    email = request.form.get('userEmail')
    phoneNumber = request.form.get('phoneNumber')
    userAddress = request.form.get('userAddress')
    realName = request.form.get('realName')

    loginUsername = request.form.get('loginUsername')
    loginPassword = request.form.get('loginPassword')

    
    # check if logged in
    if 'loggedin' in session:
        return redirect("/dashboard")

    #check if user want to login or sign up    
    elif userName:
        #form info back-end validation
        connection = getCursor()
        connection.execute('SELECT * FROM users WHERE userName = %s', (userName,))
        account = connection.fetchall()
        # If account exists show error and validation checks
        if account:
            msg = 'Failed sign up: Account already exists!'
            return render_template("index.html", msg = msg)
        elif request.form == None:
            return redirect("/")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Failed sign up: Invalid email address!'
            return render_template("index.html", msg = msg)

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
            
            msg = 'You have successfully signed up!'
            return render_template("index.html", msg = msg)
        

    elif loginUsername:
        connection = getCursor()
        connection.execute('SELECT * FROM users WHERE userName = %s', (loginUsername,))
        account = connection.fetchall()
        # If account exists show error and check password
        if not account:
            msg = 'Failed login: Account not exist or incorrect password!'
            
            return render_template("index.html", msg=msg)
        else:
            password = account[0][3]
            userPermission = account[0][1]
            if bcrypt.checkpw(loginPassword.encode('utf-8'),password.encode('utf-8')):
            # If account exists in accounts table in out database
            # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account[0][0]
                session['username'] = account[0][2]
                # Redirect to home page
                return redirect('/dashboard')
            else:
                msg = 'Failed login: Account not exist or incorrect password!'
                return render_template("index.html", msg=msg)
    
    
    return render_template("index.html")
    

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    flash('Logout successful!', 'success')

    # Redirect to login page
    return redirect("/")

@app.route('/dashboard')
def dashboard():
    # Check if user is loggedin
    if 'loggedin' in session:
        # Check permission
        
        if userInfo()[0][1] == 1:
            return render_template('dash1.html', username=session['username'])
        elif userInfo()[0][1] == 2:
            return render_template('dash2.html', username=session['username'])
        elif userInfo()[0][1] == 3:
            return render_template('dash3.html', username=session['username'])
    # User is not loggedin redirect to login page
    else:
        return redirect('/')
    
@app.route('/profile')
def profile():
    if 'loggedin' in session:
        userInfo()
        return render_template('profile.html', session=session, userEmail=userInfo()[0][2], \
                               phoneNumber=userInfo()[0][3], userAddress=userInfo()[0][4])


    else:
        return redirect('/')