from flask import render_template, request

from models.ad import CarAd
from models.user import User
from models.settings import db


def dashboard():

    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            ads = db.query(CarAd).filter_by(username=user.username).all()

            return render_template("dashboard.html", user=user, ads=ads)

    return render_template("error.html")


def post_car():
    if request.method == "GET":
        session_cookie = request.cookies.get("session")

        if session_cookie:
            user = db.query(User).filter_by(session_token=session_cookie).first()
            if user:
                return render_template("post-car.html")

        return render_template("error.html")

    elif request.method == "POST":

        brand = request.form.get("brand")
        date = request.form.get("date")
        kilometers = request.form.get("kilometers")
        horsepower = request.form.get("horsepower")
        transmission = request.form.get("transmission")
        color = request.form.get("color")
        price = request.form.get("price")
        image = request.form.get("image")
        car_model = request.form.get("car-model")

        session_cookie = request.cookies.get("session")
        if session_cookie:
            user = db.query(User).filter_by(session_token=session_cookie).first()
            if user:
                new_add = CarAd(username=user.username, brand=brand, date=date, kilometers=kilometers,
                                horsepower=horsepower, transmission=transmission, email=user.email,
                                telephone=user.phone_number, color=color, price=price, image=image, car_model=car_model)
                new_add.save()

            return render_template("successful-login.html")
        else:
            return render_template("error_2.html")

