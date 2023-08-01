from app import app, connect

from flask import render_template, request, redirect, url_for, session, flash
import re
import mysql.connector
from mysql.connector import FieldType

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
    if 'loggedin' in session and userInfo()[0][0][1] != 3:
        pass
    else:
        return redirect('/')

@app.route("/carsAdd", methods = ['POST'])
def carsAdd():
    if 'loggedin' in session and userInfo()[0][0][1] != 3:
        pass
    else:
        return redirect('/')