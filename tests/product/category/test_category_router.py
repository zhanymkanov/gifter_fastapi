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


def test_category_route_get_all(client: TestClient) -> None:
    resp = client.get("/categories")
    assert resp.status_code == 200


def test_category_route_update(client: TestClient) -> None:
    slug, title = random_lower_string(), random_lower_string()
    data_in = {
        "title": title,
        "slug": slug,
    }
    client.post("/categories", json=data_in)

    new_title = f"{title}-UPD"
    data_in.update({"title": new_title})

    resp = client.put(f"/categories/{slug}", json=data_in)
    resp_json = resp.json()

    assert resp.status_code == 200
    assert resp_json["title"] == new_title


def test_category_route_update_not_exists(client: TestClient) -> None:
    data_in = {
        "title": "title",
        "slug": "slug",
    }
    resp = client.put("/categories/not-exists", json=data_in)
    resp_json = resp.json()

    assert resp.status_code == 404
    assert resp_json["detail"] == ErrorCode.CATEGORY_SLUG_NOT_FOUND
