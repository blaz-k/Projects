from models.settings import db
from datetime import datetime


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
