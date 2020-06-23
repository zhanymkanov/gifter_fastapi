from fastapi.testclient import TestClient

from app.auth.constants import ErrorCode
from tests.utils import random_lower_string


def test_register(client: TestClient):
    user_in = {
        "email": f"{random_lower_string()}@test.net",
        "password": "hackme",
    }
    resp = client.post("auth/register", json=user_in)
    resp_json = resp.json()

    assert resp.status_code == 200
    assert resp_json["access_token"]


def test_register_already_exists(client: TestClient):
    user_in = {
        "email": f"{random_lower_string()}@test.net",
        "password": "hackme",
    }
    client.post("auth/register", json=user_in)

    resp = client.post("auth/register", json=user_in)
    resp_json = resp.json()

    assert resp.status_code == 400
    assert resp_json["detail"] == ErrorCode.REGISTER_USER_ALREADY_EXISTS


def test_logon_access_token(client: TestClient):
    email = f"{random_lower_string()}@test.net"
    user_in = {
        "email": email,
        "password": "hackme",
    }
    client.post("auth/register", json=user_in)

    user_in = {
        "username": email,
        "password": "hackme",
    }
    resp = client.post("auth/token", data=user_in)
    resp_json = resp.json()

    assert resp.status_code == 200
    assert resp_json["access_token"]


def test_logon_access_token_not_exists(client: TestClient):
    user_in = {
        "username": "not_exists@404.me",
        "password": "hackme",
    }
    resp = client.post("auth/token", data=user_in)
    resp_json = resp.json()

    assert resp.status_code == 401
    assert resp_json["detail"] == ErrorCode.LOGIN_BAD_CREDENTIALS


def test_read_users_me(client: TestClient):
    email = f"{random_lower_string()}@test.net"
    user_in = {
        "email": email,
        "password": "hackme",
    }
    resp = client.post("auth/register", json=user_in).json()
    token = resp["access_token"]

    headers = {
        "Authorization": f"Bearer {token}",
    }
    resp = client.post("/auth/users/me", headers=headers)
    resp_json = resp.json()

    assert resp.status_code == 200
    assert resp_json["email"] == email


def test_read_users_me_fail_jwt_decode(client: TestClient):
    token = "INVALID_JWT.TOKEN.OK"

    headers = {
        "Authorization": f"Bearer {token}",
    }
    resp = client.post("/auth/users/me", headers=headers)
    resp_json = resp.json()

    assert resp.status_code == 401
    assert resp_json["detail"] == ErrorCode.COULD_NOT_VALIDATE_CREDENTIALS
