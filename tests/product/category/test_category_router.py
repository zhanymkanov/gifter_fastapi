from fastapi.testclient import TestClient

from app.product.category.constants import ErrorCode
from tests.utils import random_lower_string


def test_category_route_create(client: TestClient) -> None:
    data_in = {
        "title": random_lower_string(),
        "slug": random_lower_string(),
    }
    resp = client.post("/categories", json=data_in)
    resp_json = resp.json()

    assert resp.status_code == 201
    assert resp_json["id"]


def test_category_route_create_title_exists(client: TestClient) -> None:
    data_in = {
        "title": random_lower_string(),
        "slug": random_lower_string(),
    }
    client.post("/categories", json=data_in)

    data_in.update({"slug": random_lower_string()})
    resp = client.post("/categories", json=data_in)
    resp_json = resp.json()

    assert resp.status_code == 400
    assert resp_json["detail"] == ErrorCode.CATEGORY_TITLE_ALREADY_EXISTS


def test_category_route_create_slug_exists(client: TestClient) -> None:
    data_in = {
        "title": random_lower_string(),
        "slug": random_lower_string(),
    }
    client.post("/categories", json=data_in)

    data_in.update({"title": random_lower_string()})
    resp = client.post("/categories", json=data_in)
    resp_json = resp.json()

    assert resp.status_code == 400
    assert resp_json["detail"] == ErrorCode.CATEGORY_SLUG_ALREADY_EXISTS
