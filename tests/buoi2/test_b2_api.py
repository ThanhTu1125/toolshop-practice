"""Buoi 2 - API testing with APIRequestContext (not the requests library).

Fixtures you can use (see conftest.py): api, test_user, auth_token, auth_headers
Helpers: register_user(api, email, password), new_email(), strong_password()

Run:  pytest tests/buoi2/test_b2_api.py -v
"""
import json
from pathlib import Path

import pytest

from conftest import new_email, register_user, strong_password

pytestmark = pytest.mark.api

KEYWORDS = json.loads((Path(__file__).parents[2] / "data" / "search_keywords.json").read_text())


# ---------------------------------------------------------------- B2.1 (together)
@pytest.mark.smoke
def test_b2_1_status_returns_toolshop(api):
    """Goal: API is alive.
    Precondition: none.
    Expected: 200 and app_name Toolshop."""
    response = api.get("/status")
    assert response.status == 200, response.text()
    assert response.json()["app_name"] == "Toolshop"


# ---------------------------------------------------------------- B2.2
def test_b2_2_products_first_page_has_pagination_and_product_shape(api):
    """Goal: contract of GET /products.
    Precondition: none.
    Expected: keys current_page/data/per_page/total/last_page, 0 < len(data) <= per_page,
    every product has id (str or int), a non-empty name and a price > 0."""
    response = api.get("/products", params={"page": 1})
    assert response.status == 200, response.text()
    body = response.json()
    for key in ("current_page", "data", "per_page", "total", "last_page"):
        assert key in body, f"missing key {key}"
    assert 0 < len(body["data"]) <= body["per_page"]
    for product in body["data"]:
        assert isinstance(product["id"], (str, int))
        assert isinstance(product["name"], str) and product["name"].strip()
        assert isinstance(product["price"], (int, float)) and product["price"] > 0


# ---------------------------------------------------------------- B2.3 data-driven
@pytest.mark.parametrize("case", KEYWORDS, ids=[c["keyword"] for c in KEYWORDS])
def test_b2_3_search_api_returns_only_matching_names(api, case):
    """Goal: GET /products/search?q=... filters by name.
    Precondition: none.
    Expected: at least one result and every name contains the keyword."""
    response = api.get("/products/search", params={"q": case["keyword"]})
    assert response.status == 200, response.text()
    names = [p["name"] for p in response.json()["data"]]
    assert names, f"no results for {case['keyword']}"
    assert all(case["must_contain"] in n.lower() for n in names), names


# ---------------------------------------------------------------- B2.4 errors
@pytest.mark.parametrize(
    "path, expected",
    [
        ("/users/me", 401),
        ("/products/does-not-exist", 404),
    ],
)
def test_b2_4a_protected_or_missing_resource_returns_4xx(api, path, expected):
    """Goal: unauthenticated or missing resource returns expected 4xx status.
    Precondition: unauthenticated APIRequestContext.
    Expected: GET /users/me returns 401 and GET /products/does-not-exist returns 404."""
    response = api.get(path)
    assert response.status == expected, response.text()


def test_b2_4b_register_empty_body_returns_422_with_field_errors(api):
    """Goal: server-side validation.
    Precondition: none.
    Expected: 422 and error lists for 'email' and 'password'."""
    response = api.post("/users/register", data={})
    assert response.status == 422, response.text()
    body = response.json()
    assert isinstance(body.get("email"), list) and body["email"], body
    assert isinstance(body.get("password"), list) and body["password"], body


def test_b2_4c_register_leaked_password_is_rejected(api):
    """Goal: password policy.
    Precondition: none.
    Expected: 422 because 'Welcome01!' appears in known data leaks."""
    response = register_user(api, new_email(), "Welcome01!")
    assert response.status == 422, response.text()
    body = response.json()
    assert "data leak" in " ".join(body.get("password", [])).lower(), body


# ---------------------------------------------------------------- B2.5 token
def test_b2_5a_users_me_with_token_returns_own_profile(api, auth_headers, test_user):
    """Goal: bearer token grants access.
    Precondition: user registered by the fixture.
    Expected: 200 and the same email."""
    response = api.get("/users/me", headers=auth_headers)
    assert response.status == 200, response.text()
    assert response.json()["email"] == test_user["email"]


def test_b2_5b_register_response_does_not_expose_password(api):
    """Goal: no secrets in responses.
    Precondition: none.
    Expected: 201 and no 'password' key in the JSON body."""
    response = register_user(api, new_email(), strong_password())
    assert response.status == 201, response.text()
    assert "password" not in response.json()


# ---------------------------------------------------------------- B2.6 your own fixture
@pytest.fixture
def new_cart(api):
    """Create a fresh cart via POST /carts and return its id."""
    response = api.post("/carts")
    assert response.status == 201, response.text()
    return response.json()["id"]


def test_b2_6_cart_add_product_quantity_two_is_stored(api, new_cart):
    """Goal: cart API stores the quantity.
    Precondition: a new cart (your fixture) and the first product of GET /products.
    Expected: GET /carts/{id} has exactly 1 item, quantity 2, same product_id."""
    products_resp = api.get("/products", params={"page": 1})
    assert products_resp.status == 200, products_resp.text()
    product_id = products_resp.json()["data"][0]["id"]

    add_resp = api.post(
        f"/carts/{new_cart}",
        data={"product_id": product_id, "quantity": 2},
    )
    assert add_resp.status == 200, add_resp.text()

    cart_resp = api.get(f"/carts/{new_cart}")
    assert cart_resp.status == 200, cart_resp.text()
    items = cart_resp.json()["cart_items"]
    assert len(items) == 1, items
    assert items[0]["product_id"] == product_id
    assert items[0]["quantity"] == 2
