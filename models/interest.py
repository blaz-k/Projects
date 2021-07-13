from models.settings import db
from datetime import datetime


class CarAdInterest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interest_name = db.Column(db.String, unique=False)
    interest_surname = db.Column(db.String, unique=False)
    interest_email = db.Column(db.String, unique=False)
    interest_telephone = db.Column(db.Integer, unique=False)
    ad_id = db.Column(db.Integer, unique=False)
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, onupdate=datetime.now())

