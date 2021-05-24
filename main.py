import os
from flask import Flask, render_template, request
from sqla_wrapper import SQLAlchemy


db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)
db = SQLAlchemy(db_url)


#class User


app = Flask(__name__)

#db.create_all()

# in alphabetical order

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        return render_template("registration.html")
   # elif request.method == "POST":
#dobi vse podatke iz baze
#ce user ne obstaja naredimo novega. check in base
#check if password == repeat



if __name__ == "__main__":
    app.run(use_reloader=True)