from models.settings import db
from flask import Flask
from handlers import auth, dashboard, public, ad, user


app = Flask(__name__)
db.create_all()


# AUTHENTICATION
app.add_url_rule(rule="/login", endpoint="auth.login", view_func=auth.login, methods=["GET", "POST"])
app.add_url_rule(rule="/logout", endpoint="auth.logout", view_func=auth.logout, methods=["GET"])
app.add_url_rule(rule="/registration", endpoint="auth.registration", view_func=auth.registration, methods=["GET", "POST"])

# PUBLIC
app.add_url_rule(rule="/", endpoint="public.home", view_func=public.home, methods=["GET"])
app.add_url_rule(rule="/contact", endpoint="public.contact", view_func=public.contact, methods=["GET"])
app.add_url_rule(rule="/faq", endpoint="public.faq", view_func=public.faq, methods=["GET"])
app.add_url_rule(rule="/about", endpoint="public.about", view_func=public.about, methods=["GET"])
app.add_url_rule(rule="/post-question", endpoint="public.post_question", view_func=public.post_question, methods=["GET"])


# DASHBOARD
app.add_url_rule(rule="/dashboard", endpoint="dashboard.dashboard", view_func=dashboard.dashboard, methods=["GET", "POST"])
app.add_url_rule(rule="/dashboard/post-car", endpoint="dashboard.post_car", view_func=dashboard.post_car, methods=["GET", "POST"])


# ADS
app.add_url_rule(rule="/ad/<ad_id>", endpoint="ad.ad", view_func=ad.ad, methods=["GET", "POST"])
app.add_url_rule(rule="/dashboard/ad/<ad_id>", endpoint="ad.my_ads", view_func=ad.my_ads, methods=["GET"])


# USER
app.add_url_rule(rule="/dashboard/edit-profile", endpoint="user.edit_profile", view_func=user.edit_profile, methods=["GET", "POST"])


if __name__ == "__main__":
    app.run(use_reloader=True)