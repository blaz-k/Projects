from flask import Flask, render_template

app = Flask(__name__)


# in alphabetical order

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/registration")
def registration():
    return render_template("registration.html")


if __name__ == "__main__":
    app.run(use_reloader=True)