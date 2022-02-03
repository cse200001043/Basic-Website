from flask import Flask,render_template,request,redirect,flash
from flask import *
from flask_mysqldb import MySQL
import mysql.connector

app=Flask(__name__)
app.secret_key = "qwertyuiop"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mayank.123'
app.config['MYSQL_DB'] = 'cs257_assignment_3'
mysql=MySQL(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/',methods=['POST'])
def checklogin():
    userdetails=request.form
    email=userdetails['email']
    password=userdetails['password']
    cur=mysql.connection.cursor()
    cur.execute("select * from user where email=%s and password=%s",(email,password))
    user=cur.fetchall()
    cur.close()
    if len(user)>0:
        return redirect('/home')
    else:
        cur=mysql.connection.cursor()
        cur.execute("select * from user where email=%s",(email,))
        user=cur.fetchall()
        cur.close()
        if len(user)>0:
            return "You entered wrong password"
        else:
            return "This UserId doesn't exist"
            

@app.route('/register',methods=['GET','POST'])
def index():
    if request.method=='POST':
       userdetails=request.form
       name=userdetails['name']
       email=userdetails['email']
       password=userdetails['password']
       phone=userdetails['phone']
       cur=mysql.connection.cursor()
       cur.execute("select*from user where email=%s",(email,))
       user=cur.fetchall()
       cur.close()
       if len(user)>0:
           return "Sorry this Email is already registered !"
       cur=mysql.connection.cursor()
       cur.execute("insert into user(name,email,password,phone) values(%s,%s,%s,%s)",(name,email,password,phone))
       mysql.connection.commit()
       cur.close()
       return redirect('/home')
    return render_template('sign_up.html')

@app.route('/login')
def loginpage():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('welcome.html')

@app.route('/course')
def course():
    return render_template('course.html')

if __name__ =='__main__':
    app.run(debug=True)