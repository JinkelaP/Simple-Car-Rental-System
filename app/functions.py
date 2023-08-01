from app import app, connect

from flask import render_template, request, redirect, url_for, session, flash
import re
import mysql.connector
from mysql.connector import FieldType
import os

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