from app import app

from flask import render_template, request, redirect, url_for, session, flash
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect
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

# redirect all 404 pages to my bootstrapped one.
@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html'), 404

#The index page of the web app
@app.route("/", methods=['GET','POST'])
def index():    
    userPermission = request.form.get('permission')
    userName = request.form.get('userName')
    userPassword = request.form.get('userPassword')
    email = request.form.get('userEmail')
    phoneNumber = request.form.get('phoneNumber')
    userAddress = request.form.get('userAddress')

    loginUsername = request.form.get('loginUsername')
    loginPassword = request.form.get('loginPassword')

    #check if user want to login or sign up    
    if userName:
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
            bytes = userPassword.encode('utf-8')
            salt = bcrypt.gensalt()
            hashedPsw = bcrypt.hashpw(bytes, salt)
            # create account
            connection.execute("INSERT INTO users \
                            (userPermission,userName,userPassword, \
                            email, phoneNumber, userAddress)\
                            VALUES (%s, %s, %s, %s, %s, %s);", \
                                (userPermission, userName, hashedPsw, \
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
                if userPermission == 1:
                    return render_template("dash1.html")
                elif userPermission == 2:
                    return render_template("dash2.html")
                elif userPermission == 3:
                    return render_template("dash3.html")
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

@app.route('/dashboard1')
def dashboard1():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('dash1.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect('/')