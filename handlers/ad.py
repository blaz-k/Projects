from flask import render_template, request

from models.ad import CarAd
from models.interest import CarAdInterest
from models.user import User
from models.settings import db


def ad(ad_id):
    ad = db.query(CarAd).get(int(ad_id))

    session_cookie = request.cookies.get("session")
    user = None
    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()

    ads = db.query(CarAd).all()

    if request.method == "GET":
        if not ad:
            return render_template("not-found.html", user=user)

        return render_template("ad.html", ad=ad, ads=ads, user=user)

    elif request.method == "POST":
        interest_name = request.form.get("interest-name")
        interest_surname = request.form.get("interest-surname")
        interest_email = request.form.get("interest-email")
        interest_telephone = request.form.get("interest-telephone")

        new_interest = CarAdInterest(interest_name=interest_name, interest_surname=interest_surname,
                                     interest_email=interest_email, interest_telephone=interest_telephone, ad_id=ad.id)
        new_interest.save()
        if session_cookie:
            user = db.query(User).filter_by(session_token=session_cookie).first()
            if user:
                return render_template("successful-login.html")
            if not user:
                return render_template("interest-posted.html")
    return render_template("error_2.html")


def my_ads(ad_id):
    ad = db.query(CarAd).get(int(ad_id))
    interests = db.query(CarAdInterest).filter_by(ad_id=ad_id).all()
    session_cookie = request.cookies.get("session")

    if not ad:
        return render_template("not-found-log-in.html")
    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            return render_template("dashboard-my-ads.html", user=user, ad=ad, interests=interests)
    else:
        return render_template("error.html")