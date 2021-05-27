import os
import pytest

# important: this line needs to be set BEFORE the "app" import
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from main import app, db, User


@pytest.fixture
def client():
    client = app.test_client()

    cleanup()  # clean up before every test

    db.create_all()

    yield client


def cleanup():
    # clean up/delete the DB (drop all tables in the database)
    db.drop_all()


# !!!TESTS IN ALPHABETICAL ORDER!!!

# ABOUT TESTS:
def test_about_page(client):
    response = client.get("/about")
    assert b"about us" in response.data


# DASHBOARD TESTS:
def test_dashboard_page(client):
    client.post("/registration", data={"username": "b", "password": "b", "repeat": "b"})
    client.post("/login", data={"username": "b", "password": "b"}, follow_redirects=True)
    response = client.get("/dashboard")
    assert b"Dashboard" in response.data


def test_dashboard_page_fail(client):
    response = client.get("/dashboard")
    assert b"You are not logged in!" in response.data


# HOMEPAGE TEST:
def test_home_page(client):
    response = client.get("/")
    assert b"homepage" in response.data


# CAR INTEREST TEST:
def test_interest_page_get(client):
    response = client.get("/interest")
    assert b"INTEREST" in response.data


# LOG-IN TESTS:
def test_login_page_get(client):
    response = client.get("/login")
    assert b"Remember me" in response.data


def test_login_page_post(client):
    client.post("/registration", data={"username": "b", "password": "b", "repeat": "b"})
    client.post("/login", data={"username": "b", "password": "b"}, follow_redirects=True)
    response = client.get("/dashboard")
    assert b"Dashboard" in response.data


# !!!NEVEM KAKO TO NAREDITI!!!
def test_login_page_post_fail(client):
    response = client.post("/login", data={"username": "nekaj", "password": "novega"})
    assert b"Password or username is not correct" in response.data
    user = db.query(User).filter_by(username="ne", password="novega").first()


# POST CAR TESTS
def test_post_car_page_get(client):
    client.post("/registration", data={"username": "b", "password": "b", "repeat": "b"})
    client.post("/login", data={"username": "b", "password": "b", "repeat": "b"})
    response = client.get("/dashboard/post-car")

    assert b"I want to sell a car" in response.data

"""
def test_post_car_page_post(client):
    client.post("/registration", data={"username": "b", "password": "b", "repeat": "b"})
    client.post("/login", data={"username": "b", "password": "b", "repeat": "b"})

    client.post("/dashboard/post-car", data={"brand": "ferrari", "date": "25/5/2020", "kilometers": "154", "horsepower": "110",
                                "transmission": "auto", "email": "b@b.com", "telephone": "123456", "color": "blue",
                                "price": "123456"},
                follow_redirects=True)

    response = client.get("/dashboard/post-car")
    assert b"Your post was successful" in response.data
"""

# REGISTRATION TESTS:
def test_registration_page_get(client):
    response = client.get("/registration")
    assert b"registration" in response.data


def test_registration_page_post(client):
    response = client.post("/registration", data={"username": "b", "password": "b", "repeat": "b"})
    assert b"Your registration was successful" in response.data

    user = db.query(User).filter_by(username="b").first()
    assert user is not None


def test_registration_page_post_fail(client):
    response = client.post("/registration", data={"username": "b", "password": "b", "repeat": "blaz"})

    assert b"Passwords do not match!" in response.data

    user = db.query(User).filter_by(username="b").first()
    assert user is None
