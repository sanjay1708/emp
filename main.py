#################
#API REQUIREMENTS
##################
from flask import *  
import pymysql
from app import app
from config import mysql






##################################
#FRONTEND and BACKEND REQUIREMENTS
##################################
import requests
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask import *  
from flask_mail import *  
from random import *  
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import smtplib
from flask import Flask, request, make_response
import pyrebase






######################################################
#FIREBASE CONFIGURATION for LOGIN VIA GOOGLE COMPONENT
######################################################
config = {
    "apiKey": "AIzaSyCGZtlEO7nMcNuRZ3H7YkhznQVnctJ_m8c",
    "authDomain": "certificatescape-e7ca7.firebaseapp.com",
    "projectId": "certificatescape-e7ca7",
    "storageBucket": "certificatescape-e7ca7.appspot.com",
    "messagingSenderId": "801688860458",
    "appId": "1:801688860458:web:671f8ccb033b2672f89053",
    "measurementId": "G-LRL3CWDFK0",
    "databaseURL": "your database url"  }
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()






######################################
#SMTP CONFIGURATION for EMAIL SERVICES
######################################
app = Flask(__name__)
app.config["MAIL_SERVER"]='smtp.gmail.com'  
app.config["MAIL_PORT"] = 465    
app.config["MAIL_USERNAME"] = 'certificatescape@gmail.com'  
app.config['MAIL_PASSWORD'] = 'czjj pmte kvdc abwf'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True  
otp = randint(000000,999999)  
mail = Mail(app)  






##################
#API CONSTRUCTION
##################



#CREATE API (POST)
@app.route('/create', methods=['POST'])
def create_emp():
    try:        
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _phone = _json['phone']
        _address = _json['address']	
        if _name and _email and _phone and _address and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery = "INSERT INTO emp(name, email, phone, address) VALUES(%s, %s, %s, %s)"
            bindData = (_name, _email, _phone, _address)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Employee added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()          
        
        
        
#VIEW API (GET)
@app.route('/emp')
def emp():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, email, phone, address FROM emp")
        empRows = cursor.fetchall()
        for i in range (0, len(empRows)):
            respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  
        
        
        
#VIEW INDIVIDUAL API (GET)
@app.route('/emp/<int:emp_id>')
def emp_details(emp_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, email, phone, address FROM emp WHERE id =%s", emp_id)
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()


        
#UPDATE API (PUT)
@app.route('/update', methods=['PUT'])
def update_emp():
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _email = _json['email']
        _phone = _json['phone']
        _address = _json['address']
        if _name and _email and _phone and _address and _id and request.method == 'PUT':			
            sqlQuery = "UPDATE emp SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s"
            bindData = (_name, _email, _phone, _address, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Employee updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 
        
        
        
#DELETE API (DELETE)
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_emp(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM emp WHERE id =%s", (id,))
		conn.commit()
		respone = jsonify('Employee deleted successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
        
        
        
#ERROR HANDLER API       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
    
    



    
#############################
#LOGIN REGISTRATION COMPONENT
#############################


#DATABASE CONFIGURAATIONS   
app.config['MYSQL_HOST'] = "remotemysql.com"
app.config['MYSQL_USER'] = "ScuRX0z6Nb"
app.config['MYSQL_PASSWORD'] = "o6CJSRnS75"
app.config['MYSQL_DB'] = "ScuRX0z6Nb" 
app.config["SECRET_KEY"] = "random secret key"    
mysqll = MySQL(app)
mail = Mail(app)  


#LOGIN COMPONENT
@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['password']
        cursor = mysqll.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password ))
        account = cursor.fetchone()
        print(account)
        print(account[-1])
        if account:
            if account[-1]==1:
                session['loggedin'] = True
                session['id'] = account[0]
                userid=  account[0]
                session['username'] = account[1]
                msg = 'Logged in successfully !'
                return render_template('expense.html', msg = msg)
            elif account[-1]==0:             
                msg = Message('OTP',sender = 'certificatescape@gmail.com', recipients = [email])  
                msg.body = str(otp)  
                mail.send(msg)   
                return render_template('verify.html') 
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)


#REGISTER COMPONENT    
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        auth = 0
        cursor = mysqll.connection.cursor()
        cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            #url = "http://127.0.0.1:5001/?name="+username+"&recId="+email
            #requests.get(url)
            msg = 'You have successfully registered !'
            msg = Message('OTP',sender = 'certificatescape@gmail.com', recipients = [email])  
            msg.body = str(otp)  
            mail.send(msg)  
            ack = Message('Welcome!',sender = 'certificatescape@gmail.com', recipients = [email])
            ack.body = "Welcome to Insite+ "+username+", kindly confirm your email ID by enrolling the One-Time Password sent to your account. Thank you!"
            mail.send(ack)  
            cursor.execute('INSERT INTO user VALUES (% s, % s, % s, % s)', (username, email,password, auth))
            mysqll.connection.commit()
           
            return render_template('verify.html') 
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)
    
    
#FORGOT YOUR PASSWORD VERIFICATION COMPONENT    
@app.route('/registerr', methods =['GET', 'POST'])
def registerr():
    msg = ''
    if request.method == 'POST' :
        email = request.form['email']
        msg = Message('OTP',sender = 'certificatescape@gmail.com', recipients = [email])  
        msg.body = str(otp)  
        mail.send(msg)  
        return render_template('verifyy.html') 
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('registerr.html', msg = msg)
    
    
#UPDATE YOUR PASSWORD COMPONENT    
@app.route('/registerrr', methods =['GET', 'POST'])
def registerrr():
    msg = ''
    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['password']       
        cursor = mysqll.connection.cursor()
        cursor.execute('UPDATE user SET password = % s WHERE email = % s', (password,email))
        mysqll.connection.commit()
        msg = "Password updated successfully!"
        return render_template('login.html', msg=msg)           
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('registerrr.html', msg = msg)
    
    
#OTP VERIFICATION COMPONENT for REGISTER    
@app.route('/validate',methods=["POST"])   
def validate():  
    user_otp = request.form['otp']  
    if otp == int(user_otp):       
         msg="Email verification successful"
         cursor = mysqll.connection.cursor()
         auth = 1
         old = 0
         cursor.execute('UPDATE user SET auth = % s WHERE auth = % s', (auth,old))
         mysqll.connection.commit()
         return render_template('login.html', msg = msg) 
    return "<h3>failure, OTP does not match</h3>"   


#OTP VERIFICATION COMPONENT for FORGOT PASSWORD
@app.route('/verifyy', methods =['GET', 'POST'])
def verifyyy():
    user_otp = request.form['otp']  
    if otp == int(user_otp):       
         msg="Email verification successful"

         return render_template('registerrr.html', msg=msg) 
    return "<h3>failure, OTP does not match</h3>"   


####################    
#FRONTEND COMPONENT
####################



#LANDING PAGEv1
@app.route('/')
def home():
	    return render_template('home.html')      
      



#LANDING PAGEv2      
@app.route('/home')
def homee():
	    return render_template('home.html')  

        
        
#DASHBOARD        
@app.route('/dashboard')
def expensee():
	    return render_template('expense.html')
        
        
        
        
        
               
###################               
#FRONTEND CONNECTS
###################

               
#VIEW EMPLOYEES API FRONTEND CONNECT   
@app.route('/empp', methods =['GET', 'POST'])
def empp():
    return render_template("allemp.html")
    
    
#CREATE API FRONTEND CONNECT    
@app.route('/createe', methods =['GET', 'POST'])
def applya():
    msg = ''
    if request.method == 'POST' :
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        url = 'http://127.0.0.1:5000/create' #API CALL
        myobj = {'name': name,
                 'email' : email,
                 'address' : address,
                 'phone' : phone}
        x = requests.post(url, json = myobj)  
        msg = "Details added successfully"
        ack = Message('Details created successfully!',sender = 'certificatescape@gmail.com', recipients = [email])
        ack.body = "Congrats "+name+"! You have successfully added your Employment Details."
        mail.send(ack)  
    return render_template('application.html',msg = msg)
 

#UPDATE API FRONTEND CONNECT 
@app.route('/updatee', methods =['GET', 'POST', 'PUT'])
def updatee():
    if request.method == 'PUT' or request.method == 'POST'  :
        id = request.form['id']
        email = request.form['email']
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        myobj = {"address": address,
                "email": email,
                "id": id,
                "name": name,
                "phone": phone}
        url = 'http://127.0.0.1:5000/update' #API CALL
        response = requests.put(url, json=myobj)
        flash("Details updated successfully")
        ack = Message('Details updated successfully!',sender = 'certificatescape@gmail.com', recipients = [email])
        ack.body = "Congrats "+name+"! You have successfully updated your Employment Details."
        mail.send(ack)  
    return render_template('update.html') 
    
    
#DELETE API FRONTEND CONNECT    
@app.route('/deletee', methods =['GET', 'POST', 'DELETE'])    
def deletee():
    if request.method == 'DELETE' or request.method == 'POST'  :
        id = request.form['id']
        email = request.form['email']
        con = mysqll.connection.cursor()

        con.execute('select email from emp where id=%s', (id,))
        account = con.fetchone()
        print(account)
        if account[0]==email:
            myobj = {"id": id, "email":email}
            url = 'http://127.0.0.1:5000/delete/'+id #API CALL
            response = requests.delete(url)
            flash("Details deleted successfully")
            ack = Message('Deletion Notice!',sender = 'certificatescape@gmail.com', recipients = [email])
            ack.body = "You have successfully deleted your Employment details."
            mail.send(ack) 
        else:
            flash("Wrong email!")
            
    return render_template('delete.html')       
    
    
   
#SEARCH USING ANY KEYWORD COMPONENT
@app.route('/search',methods =['GET', 'POST'])
def applyc():
    msg=''
    cursor = mysqll.connection.cursor()
    mycursor = mysqll.connection.cursor()
    if request.method=='POST':
       search=request.form['search']
       print(search)     
       cursor = mysqll.connection.cursor()
       cursor.execute('SELECT * FROM emp WHERE id = % s', ( search,))
       msg = "filtering your search by keyword "+search

       usercerf = cursor.fetchall()
       print(usercerf)
       return render_template('survey1.html',usercerf=usercerf)
    return render_template('survey1.html')
    

#APP DEPLOYMENT ON PORT 8000 AS PER REQUIREMENT    
if __name__ == "__main__":
    app.run(debug=True)