import os
import pytest

# important: this line needs to be set BEFORE the "app" import
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from main import app, db


@pytest.fixture
def client():
    client = app.test_client()

    cleanup()  # clean up before every test

    db.create_all()

    yield client


def cleanup():
    # clean up/delete the DB (drop all tables in the database)
    db.drop_all()


# tests in alphabetical order


# about test:
def test_about_page(client):
    response = client.get("/about")
    assert b"about us" in response.data


# homepage tests:
def test_home_page(client):
    response = client.get("/")
    assert b"homepage" in response.data


# log-in tests:
def test_login_page(client):
    response = client.get("/login")
    assert b"Remember me" in response.data


# registration tests:
def test_registration_page(client):
    response = client.get("/registration")
    assert b"registration" in response.data


# dashboard tests:
def test_dashboard_page(client):
    response = client.get("/dashboard")
    assert b"Dashboard" in response.data
