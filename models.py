import os
from sqla_wrapper import SQLAlchemy
from datetime import datetime


db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    first_name = db.Column(db.String, unique=False)
    last_name = db.Column(db.String, unique=False)
    country = db.Column(db.String, unique=False)
    postal_code = db.Column(db.Integer, unique=False)
    email = db.Column(db.String, unique=True)
    phone_number = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=False)
    session_token = db.Column(db.String, unique=False)
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, onupdate=datetime.now())


class CarAd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=False)
    brand = db.Column(db.String, unique=False)
    date = db.Column(db.String, unique=False)
    kilometers = db.Column(db.Integer, unique=False)
    horsepower = db.Column(db.Integer, unique=False)
    transmission = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=False)
    telephone = db.Column(db.Integer, unique=False)
    color = db.Column(db.String, unique=False)
    price = db.Column(db.Integer, unique=False)
    image = db.Column(db.String, unique=False)
    car_model = db.Column(db.String, unique=False)
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, onupdate=datetime.now())


class CarAdInterest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interest_name = db.Column(db.String, unique=False)
    interest_surname = db.Column(db.String, unique=False)
    interest_email = db.Column(db.String, unique=False)
    interest_telephone = db.Column(db.Integer, unique=False)
    ad_id = db.Column(db.Integer, unique=False)
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, onupdate=datetime.now())


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_name = db.Column(db.String, unique=False)
    question_text = db.Column(db.String, unique=False)

