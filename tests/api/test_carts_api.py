import pytest

pytestmark = pytest.mark.api


@pytest.fixture
def new_cart(api):
    """Create a fresh cart via POST /carts and return its id."""
    response = api.post("/carts")
    assert response.status == 201, response.text()
    return response.json()["id"]


def test_cart_add_product_quantity_two_is_stored(api, new_cart):
    """Goal: cart API stores the quantity.
    Precondition: a new cart (new_cart fixture) and the first product of GET /products.
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
