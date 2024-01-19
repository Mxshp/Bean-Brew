from flask import Flask, render_template, request, session, redirect, url_for, flash
import time

from sqlalchemy.orm import relationship

from extension import db

from datetime import datetime as dt
from sqlalchemy import Column, Integer, DateTime

from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user

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

class Food(db.Model):
    food_id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.Unicode(64))
    food_price = db.Column(db.Numeric(10,2), nullable=False)
    food_type = db.Column(db.String(30), nullable=False)

def __unicode__(self):
    return f'<Food {self.food_name}>'

@login_manager.user_loader
def load_food(food_id):
    return Food.query.get(int(food_id))

def __str__(self):
     return self.fname

@app.route('/')
def index():
    #return redirect(url_for("check_database"))
    return render_template('index.html', current_user=current_user)

@app.route('/menu', methods=["POST", "GET"])
def menu():
    foods = Food.query.all()
    return render_template("menu.html", foods=foods)



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

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["pass"]
        customer = Customer.query.filter_by(email=email).first()
        if customer and customer.password == password:
            login_user(customer)
            flash(f"Welcome back, {customer.fname}!", "success")
            return redirect(url_for('index', customer=current_user))
        else:
            return render_template('login.html',
                                   info="Invalid details, please try again.")

    return render_template('login.html', user=current_user)

@app.route('/locations')
def locations():
    return render_template('locations.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/check_database')
def check_database():
    customers = Food.query.all()
    for food in customers:
        print(f"Food ID: {food.food_id}, Name: {food.food_name}, Type: {food.food_type}, Price: {food.food_price}")

    return "Check your console for database contents."

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
