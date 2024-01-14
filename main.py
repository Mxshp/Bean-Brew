from flask import Flask, render_template, request, session, redirect, url_for, flash
import time

from sqlalchemy.orm import relationship

from extension import db
from flask_login import UserMixin

from datetime import datetime as dt
from sqlalchemy import Column, Integer, DateTime

from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
login_manager = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

'''@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))'''

@login_manager.user_loader
def load_customer(id):
    return Customer.query.get(int(id))

class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)

def __str__(self):
     return self.fname

@app.route('/')
def index():
    #return redirect(url_for("check_database"))
    return render_template('index.html')


@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        name = request.form["fname"]
        email = request.form["email"]
        password = request.form["pass"]
        repassword = request.form["repass"]

        existing_email = Customer.query.filter_by(email=email).first()

        if password != repassword:
            return render_template('signup.html',
                                   info="The passwords don't match.")
        elif existing_email and existing_email.email == email:
            return render_template('signup.html',
                                    info="This email already exists.")
        else:
            new_customer = Customer(fname=name, email=email, password=password)
            db.session.add(new_customer)
            db.session.commit()
            return render_template('login.html')


    return render_template("signup.html")      

@app.route('/login.html', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["pass"]
        customer = Customer.query.filter_by(email=email).first()
        if customer and customer.password == password:
            login_user(customer)
            return redirect(url_for('index'))
        else:
            return render_template('login.html',
                                   info="Invalid details, please try again.")

    return render_template('login.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/locations')
def locations():
    return render_template('locations.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/check_database')
def check_database():
    customers = Customer.query.all()
    for customer in customers:
        print(f"Customer ID: {customer.id}, Name: {customer.fname}, Email: {customer.email}, Password: {customer.password}")

    return "Check your console for database contents."

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)