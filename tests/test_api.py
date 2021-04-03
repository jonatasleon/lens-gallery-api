import json
import os

import pytest
from flask.app import Flask

import core
from core.models.user import UserModel


@pytest.fixture
def app() -> Flask:
    os.environ["APP_SETTINGS"] = "../settings.cfg"
    app = core.create_app("test")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app: Flask):
    with app.app_context():
        app.db.create_all()
        user = UserModel(email="test@client.local", name="John Doe", password="12345")
        app.db.session.add(user)
        app.db.session.commit()
        yield app.test_client()
        app.db.drop_all()


@pytest.fixture
def access_token(client) -> str:
    rv = client.post(
        "/api/login",
        data=json.dumps(
            {
                "email": "test@client.local",
                "password": "12345",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(rv.data.decode())
    return data["access_token"]


@pytest.fixture
def auth_header(access_token):
    return {"Authorization": f"Bearer {access_token}"}


class TestUser:
    path = "/api/users"

    def test_when_make_a_post_with_a_correct_user_object_return_201_as_status_code(self, client):
        rv = client.post(
            self.path,
            data=json.dumps(
                {
                    "email": "another@client.com",
                    "name": "Tester",
                    "password": "12345",
                }
            ),
            content_type="application/json",
        )

        assert 201 == rv.status_code

    def test_when_make_a_post_with_an_incomplete_but_valid_user_object_return_201_as_status_code(self, client):
        rv = client.post(
            self.path,
            data=json.dumps(
                {
                    "email": "another@client.com",
                    "password": "12345",
                }
            ),
            content_type="application/json",
        )

        assert 201 == rv.status_code

    def test_when_make_a_post_to_users_without_password_return_422_as_status_code(self, client):
        rv = client.post(
            self.path,
            data=json.dumps(
                {
                    "email": "another@client.com",
                    "name": "Tester",
                }
            ),
            content_type="application/json",
        )

        assert 422 == rv.status_code

    def test_when_post_an_invalid_user_params_return_422_as_status_code(self, client):
        rv = client.post(
            self.path,
            data=json.dumps(
                {
                    "mail": "another@client.com",
                    "username": "Tester",
                }
            ),
            content_type="application/json",
        )

        assert 422 == rv.status_code

    def test_when_make_a_post_with_a_correct_user_object_return_a_valid_user_representation(self, client):
        rv = client.post(
            self.path,
            data=json.dumps(
                {
                    "email": "another@client.com",
                    "name": "Tester",
                    "password": "12345",
                }
            ),
            content_type="application/json",
        )
        data = json.loads(rv.data.decode())
        assert dict(data, email="another@client.com", name="Tester") == data
        assert "id" in data

    def test_when_try_get_user_data_with_no_credentials_return_401_status_code(self, client):
        rv = client.get(self.path)
        assert 401 == rv.status_code


class TestLogin:
    path = "/api/login"

    def test_when_try_login_with_correct_credentials_return_200_as_status_code(self, client):
        rv = client.post(
            self.path,
            data=json.dumps(
                {
                    "email": "test@client.local",
                    "password": "12345",
                }
            ),
            content_type="application/json",
        )
        assert 200 == rv.status_code

    def test_when_try_login_with_correct_credentials_return_access_token_in_body(self, client):
        rv = client.post(
            self.path,
            data=json.dumps(
                {
                    "email": "test@client.local",
                    "password": "12345",
                }
            ),
            content_type="application/json",
        )
        data = json.loads(rv.data.decode())
        assert "access_token" in data

    def test_when_try_login_with_incorrect_password_return_401_as_status_code(self, client):
        rv = client.post(
            self.path,
            data=json.dumps(
                {
                    "email": "test@client.local",
                    "password": "incorrect",
                }
            ),
            content_type="application/json",
        )
        assert 401 == rv.status_code

    def test_when_try_login_with_incorrect_email_return_401_as_status_code(self, client):
        rv = client.post(
            self.path,
            data=json.dumps(
                {
                    "email": "invalid@client.local",
                    "password": "12345",
                }
            ),
            content_type="application/json",
        )
        assert 401 == rv.status_code

    def test_when_try_login_with_invalid_params_return_422_as_status_code(self, client):
        rv = client.post(
            self.path,
            data=json.dumps(
                {
                    "mail": "invalid@client.local",
                    "passwd": "12345",
                }
            ),
            content_type="application/json",
        )
        assert 422 == rv.status_code


class TestPhoto:
    path = "/api/photos"

    def test_when_make_a_post_with_a_correct_photo_object_return_201_as_status_code(self, client, auth_header):
        rv = client.post(
            self.path,
            data=json.dumps(
                {
                    "title": "Test 1",
                    "url": "https://homepages.cae.wisc.edu/~ece533/images/goldhill.png",
                    "description": "Lorem Ipsum",
                }
            ),
            content_type="application/json",
            headers=auth_header,
        )
        assert rv.status_code == 201

    def test_when_make_a_post_with_a_correct_photo_object_return_a_valid_photo_representation(
        self, client, auth_header
    ):
        rv = client.post(
            "/api/photos",
            data=json.dumps(
                {
                    "title": "Test 1",
                    "url": "https://homepages.cae.wisc.edu/~ece533/images/goldhill.png",
                    "description": "Lorem Ipsum",
                }
            ),
            content_type="application/json",
            headers=auth_header,
        )
        data = json.loads(rv.data.decode())
        assert (
            dict(
                data,
                title="Test 1",
                url="https://homepages.cae.wisc.edu/~ece533/images/goldhill.png",
                description="Lorem Ipsum",
            )
            == data
        )
        assert "id" in data
