from models import db, User, CarAd, CarAdInterest, Questions
from flask import Flask, render_template, request, redirect, url_for, make_response
from hashlib import sha256
import uuid

app = Flask(__name__)
db.create_all()


# in alphabetical  order
@app.route("/about")
def about():
    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            return render_template("about.html", user=user)
    return render_template("about.html")


# kako nardit, ce logiran uporabnik hoce en post s stevilko ki ne obstaja??
@app.route("/ad/<ad_id>", methods=["GET", "POST"])
def ad(ad_id):
    ad = db.query(CarAd).get(int(ad_id))
    session_cookie = request.cookies.get("session")
    ads = db.query(CarAd).all()

    if request.method == "GET":
        if not ad:
            return render_template("not-found.html")
        if session_cookie:
            user = db.query(User).filter_by(session_token=session_cookie).first()
            if user:
                return render_template("ad.html", ad=ad, ads=ads, user=user)
            if not user:
                return render_template("ad.html", ad=ad, ads=ads)

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


@app.route("/contact")
def contact():
    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            return render_template("contact.html", user=user)
    return render_template("contact.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            ads = db.query(CarAd).filter_by(username=user.username).all()

            return render_template("dashboard.html", user=user, ads=ads)

    return render_template("error.html")


@app.route("/dashboard/ad/<ad_id>")
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


@app.route("/dashboard/edit-profile", methods=["GET", "POST"])
def dashboard_edit_profile():
    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()

        if not user:
            return render_template("error.html")

    else:
        return render_template("error.html")

    if request.method == "GET":
        return render_template("dashboard-edit-profile.html", user=user)

    if request.method == "POST":
        username = request.form.get("username")
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        country = request.form.get("country")
        postal_code = request.form.get("postal-code")
        email = request.form.get("user-email")
        telephone = request.form.get("telephone")
        password = request.form.get("password")
        repeat = request.form.get("repeat")

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.country = country
        user.postal_code = postal_code
        user.email = email
        user.telephone = telephone
        user.password = sha256(password.encode("utf-8")).hexdigest()
        user.repeat = repeat
        user.save()

        return redirect(url_for("dashboard"))


@app.route("/faq")
def faq():
    questions = db.query(Questions).all()
    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            return render_template("faq.html", user=user, questions=questions)
    return render_template("faq.html", questions=questions)
    

@app.route("/")
def home():
    ads = db.query(CarAd).all()
    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            return render_template("index.html", ads=ads, user=user)

    return render_template("index.html", ads=ads)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        # get username and password
        username = request.form.get("username")
        password = request.form.get("password")

        # check for password hash
        password_hash = sha256(password.encode("utf-8")).hexdigest()
        # check if username exists
        existing_user = db.query(User).filter_by(username=username, password=password_hash).first()

        # if it does exists than give him session token and set cookie
        if existing_user:
            session_token = str(uuid.uuid4())
            existing_user.session_token = session_token
            existing_user.save()

            response = make_response(redirect(url_for("dashboard")))
            response.set_cookie("session", session_token)
            return response
        else:
            return render_template("error-login.html")
    return redirect(url_for("dashboard"))


@app.route("/logout", methods=["GET"])
def logout():
    session_cookie = request.cookies.get("session")
    user = db.query(User).filter_by(session_token=session_cookie).first()
    user.session_token = ""
    user.save()

    return redirect(url_for("login"))


@app.route("/dashboard/post-car", methods=["GET", "POST"])
def post_car():
    if request.method == "GET":
        session_cookie = request.cookies.get("session")

        if session_cookie:
            user = db.query(User).filter_by(session_token=session_cookie).first()
            if user:
                return render_template("post-car.html")

        return render_template("error.html")

    elif request.method == "POST":
        # mors dobit vse podatke vn
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


@app.route("/post-question", methods=["GET", "POST"])
def post_question():
    session_cookie = request.cookies.get("session")
    question_name = request.form.get("question-name")
    question_text = request.form.get("question-text")

    if request.method == "GET":
        if session_cookie:
            user = db.query(User).filter_by(session_token=session_cookie).first()
            if user:
                return render_template("post-question.html", user=user)
            if not user:
                return render_template("post-question.html")

    elif request.method == "POST":
        if session_cookie:
            user = db.query(User).filter_by(session_token=session_cookie).first()
            if user:
                new_question = Questions(question_name=question_name, question_text=question_text)
                new_question.save()
                return render_template("successful-login.html")
            if not user:
                new_question = Questions(question_name=question_name, question_text=question_text)
                new_question.save()
                return render_template("post-successful.html")
    return render_template("error_2.html")


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        return render_template("registration.html")

    elif request.method == "POST":
        # dobi vse podatke iz baze
        username = request.form.get("username")
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        country = request.form.get("country")
        postal_code = request.form.get("postal-code")
        email = request.form.get("user-email")
        phone_number = request.form.get("telephone")
        password = request.form.get("password")
        repeat = request.form.get("repeat")
        # ce user ne obstaja naredimo novega. check in base
        existing_user = db.query(User).filter_by(username=username).first()

        if existing_user:
            return "ERROR: This username already exist! You need to choose something else."
        else:
            # check if password == repeat
            if password == repeat:
                # camouflage password
                password_hash = sha256(password.encode("utf-8")).hexdigest()
                new_user = User(username=username, first_name=first_name, last_name=last_name,
                                country=country, postal_code=postal_code, email=email,
                                phone_number=phone_number, password=password_hash)
                new_user.save()

                return render_template("successful.html")
            else:
                return render_template("passwords-not-match.html")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(use_reloader=True)