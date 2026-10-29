from flask import Flask , render_template, request, redirect, url_for, session
import requests
import re
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost:3306/good_life?charset=utf8'
db=SQLAlchemy(app)
app.secret_key = "mykey"

#contact us page table contains name, email, and message
class Contact(db.Model):
    __tablename__="contact"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30), nullable=False)
    email=db.Column(db.String(30), unique=True)
    message=db.Column(db.String(200), nullable=False)

#sign up page table contains user details name, email, profession and password
class Registration(db.Model):
    __tablename__="registration"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30), nullable=False)
    email=db.Column(db.String(30), unique=True)
    profession=db.Column(db.String(30), nullable=False)
    password=db.Column(db.String(30),nullable=False)

#regex for name, password and email
txt=r'^[A-Za-z]{3,}$'
passs = r'^[A-Z][A-Za-z0-9_$@]{7,19}$'
mail = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

@app.route('/')
def index():
    return render_template("index.html")
@app.route("/story")
def story():
    return render_template("story.html")
@app.route("/epk")
def epk():
    return render_template("epk.html")
@app.route("/trailer")
def trailer():
    return render_template("trailer.html")
@app.route("/bts")
def bts():
    return render_template("bts.html")
@app.route("/filmmakers")
def filmmakers():
    return render_template("filmmakers.html")

#contact us page
@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method=="GET":
        return render_template("contact.html")
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("mail")
        message=request.form.get("message")
        #checking user entered values
        if not name or not email or not message:
            msg="Please fill empty fields"
            return render_template("contact.html", msg=msg)
        if not re.fullmatch(txt, name):
            msg="Name should contain 3+ characters"
            return render_template("contact.html", msg=msg)
        if not re.fullmatch(mail, email):
            msg="Email should be in this format xyz@xyz.xyz"
            return render_template("contact.html", msg=msg)
        #adding user value to table Contact
        else:
            entry= Contact(name=name, email=email, message=message)
            db.session.add(entry)
            db.session.commit()
            msg='Message Sent Successfully'
            return render_template("contact.html", smsg=msg)
    else:
        print("error")

# registration page 
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method=="GET":
        return render_template("register.html")
    if request.method=="POST":
        #getting user entered values
        name=request.form.get("name")
        email=request.form.get("mail")
        profession=request.form.get("profession")
        password=request.form.get("password")
        cpassword=request.form.get("cpassword")
        #checking values entered values
        if not name or not email or not profession or not password or not cpassword:
            msg="Please fill empty fields"
            return render_template("register.html", msg=msg)
        if not re.fullmatch(txt, name):
            msg="Name should contain 3+ characters"
            return render_template("register.html", msg=msg)
        if not re.fullmatch(mail, email):
            msg="Email should be in this format xyz@xyz.xyz"
            return render_template("register.html", msg=msg)
        if not re.fullmatch(passs,password):
            msg="Password should be 8 or more characters and must include capital letter in begining"
            return render_template("register.html", msg=msg)
        if password!=cpassword:
            msg="password not match"
            return render_template("register.html", msg=msg)
        #adding values to table Registration
        else:
            entry= Registration(name=name, email=email, profession=profession, password=password)
            db.session.add(entry)
            db.session.commit()
            msg='Registration Successful'
            return render_template("register.html", smsg=msg)
    else:
        print("error")

#log in page
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        #checking user entered values
        if not email or not password:
            msg="Please fill empty fields"
            return render_template("login.html", msg=msg)
        if not re.fullmatch(mail,email):
            msg="Enter valid email"
            return render_template("login.html", msg=msg)
        if not re.fullmatch(passs, password):
            msg="Enter valid Password"
            return render_template("login.html", msg=msg)
        #Checking values in table 
        user= Registration.query.filter_by(email=email, password=password).first()
        #if true login successful
        if user:
            session['email']=user.email
            msg="Login Successful"
            return render_template("login.html", smsg=msg)
        #if false invalid details
        else:
            msg="Invalid user details"
            return render_template("login.html",msg=msg)
    else:
         print("error")
if __name__=="__main__": 
    app.run(debug=True)