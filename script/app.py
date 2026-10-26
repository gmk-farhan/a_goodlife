from flask import Flask , render_template, request, redirect, url_for, session
import requests
import re
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost:3306/good_life?charset=utf8'
db=SQLAlchemy(app)
app.secret_key = "mykey"

txt=r'^[A-Za-z]{3,}$'
phonep = r'^07[0-9]{9}$'
user=r'^[A-Za-z0-9_$@]{8,20}$'
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
@app.route("/contact")
def contact():
    return render_template("contact.html")