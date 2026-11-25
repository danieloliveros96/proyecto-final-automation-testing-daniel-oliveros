"""Pruebas de API sobre JSONPlaceholder (https://jsonplaceholder.typicode.com)."""
import pytest
import requests

from utils.config import API_BASE_URL
from utils.logger import get_logger

log = get_logger("api")
TIMEOUT = 10


def _request(method, path, **kwargs):
    url = f"{API_BASE_URL}{path}"
    log.info("%s %s", method.upper(), url)
    response = requests.request(method, url, timeout=TIMEOUT, **kwargs)
    log.info("Respuesta: %s", response.status_code)
    return response


@pytest.mark.api
def test_get_post_ok():
    response = _request("get", "/posts/1")
    assert response.status_code == 200
    body = response.json()
    assert set(body) >= {"userId", "id", "title", "body"}
    assert body["id"] == 1


@pytest.mark.api
@pytest.mark.negative
def test_get_post_not_found():
    response = _request("get", "/posts/99999")
    assert response.status_code == 404
    assert response.json() == {}


@pytest.mark.api
def test_create_post():
    payload = {"title": "mi post", "body": "contenido de prueba", "userId": 1}
    response = _request("post", "/posts", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]
    assert "id" in body


@pytest.mark.api
def test_delete_post():
    response = _request("delete", "/posts/1")
    assert response.status_code == 200
    assert response.json() == {}


@pytest.mark.api
def test_chained_requests_user_and_posts():
    """Encadenamiento: se obtiene un usuario y su id se usa en la 2da petición."""
    user_response = _request("get", "/users/1")
    assert user_response.status_code == 200
    user_id = user_response.json()["id"]

    posts_response = _request("get", "/posts", params={"userId": user_id})
    assert posts_response.status_code == 200
    posts = posts_response.json()
    assert len(posts) > 0
    assert all(post["userId"] == user_id for post in posts)
