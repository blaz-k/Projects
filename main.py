import os
from flask import Flask, render_template
from sqla_wrapper import SQLAlchemy


#db_url = os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1)
#db = SQLAlchemy(db_url)


app = Flask(__name__)


# in alphabetical order

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/registration")
def registration():
    return render_template("registration.html")


if __name__ == "__main__":
    app.run(use_reloader=True)