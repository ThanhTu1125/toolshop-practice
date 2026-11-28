"""Flaky clinic (buoi 4, exercise B4.1). Five sick tests. Diagnose, then cure.

Run each patient several times and watch it flicker:
  for i in 1 2 3 4 5; do pytest clinic -q -p no:randomly; done
Patient 3 also: run it alone, and run it in parallel:
  pytest clinic/test_clinic.py::test_patient3_b_add_product_to_the_same_cart
  pytest clinic -n 2

For every patient write down: symptom, cause, cure. The cure must not use sleep.
"""
import pytest
from playwright.sync_api import expect

from conftest import new_email, register_user, strong_password
from pages.home_page import PRODUCT_LIST, HomePage


# Patient 1 - "it passes when I debug it step by step"
def test_patient1_search_hammer(page):
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    home.search("hammer")
    expect(home.search_completed).to_be_visible()
    names = home.product_names.all_inner_texts()
    assert names and all("hammer" in n.lower() for n in names), names


# Patient 2 - "I added a sleep and now it works on my laptop"
def test_patient2_sort_price_desc(page):
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    with page.expect_response(lambda r: PRODUCT_LIST.search(r.url) is not None):
        home.sort_by("price,desc")
    expect(home.sorting_completed).to_be_visible()
    prices = home.prices()
    assert prices == sorted(prices, reverse=True), prices


# Patient 3 - "green in the full run, red when I run it alone or in CI"
@pytest.fixture
def cart_id(api):
    response = api.post("/carts")
    return response.json()["id"]


def test_patient3_a_create_cart(cart_id):
    assert cart_id


def test_patient3_b_add_product_to_the_same_cart(api, cart_id):
    product = api.get("/products", params={"page": 1}).json()["data"][0]
    response = api.post(f"/carts/{cart_id}", data={"product_id": product["id"], "quantity": 1})
    assert response.ok, response.text()


# Patient 4 - "it was green yesterday"
def test_patient4_register_clinic_user(api):
    response = register_user(api, new_email(), strong_password())
    assert response.status == 201, response.text()


# Patient 5 - "red on CI, green on my machine, sometimes red on my machine too"
def test_patient5_price_slider_max_20(page):
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    home.price_slider_max.focus()
    for _ in range(4):
        with page.expect_response(lambda r: PRODUCT_LIST.search(r.url) is not None) as last:
            page.keyboard.press("PageDown")
    expected = [p["name"] for p in last.value.json()["data"]]
    expect(home.product_names).to_have_text(expected)
    prices = home.prices()
    assert all(p <= 20 for p in prices), prices
