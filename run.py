from flask import Flask, render_template, request, redirect, url_for, session
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__, static_folder='static')

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
                

# redirect all 404 pages to my bootstrapped one.
@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html'), 404

#The index page of the web app
@app.route("/")
def home():
    return render_template("index.html")

#Registration page
@app.route("/")
def signUp():
    return render_template("index.html")

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return render_template("index.html")

@app.route('/dashboard1')
def dashboard1():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('dash1.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))