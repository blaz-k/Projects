from flask import render_template, request

from models.ad import CarAd
from models.questions import Questions
from models.user import User
from models.settings import db


def about():
    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            return render_template("about.html", user=user)
    return render_template("about.html")


def home():
    ads = db.query(CarAd).all()
    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            return render_template("index.html", ads=ads, user=user)

    return render_template("index.html", ads=ads)

def faq():
    questions = db.query(Questions).all()
    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            return render_template("faq.html", user=user, questions=questions)
    return render_template("faq.html", questions=questions)


def contact():
    session_cookie = request.cookies.get("session")

    if session_cookie:
        user = db.query(User).filter_by(session_token=session_cookie).first()
        if user:
            return render_template("contact.html", user=user)
    return render_template("contact.html")


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




