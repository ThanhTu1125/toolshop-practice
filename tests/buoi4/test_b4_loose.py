"""Buoi 4 - LOOSE assertions. Every test here is green on PROD *and* on BUGGY.

That is the problem: BUGGY has real defects in exactly these features, and this suite misses all of them.

Exercise B4.4: for each test, tighten the assertion so that it
  - stays green on PROD,
  - turns red on BUGGY,
  - and the failure message tells a developer what is wrong.
Do NOT add new tests to reach a number. Strengthen the expectation.

Run on BUGGY:
  BASE_URL=https://with-bugs.practicesoftwaretesting.com API_URL=https://api-with-bugs.practicesoftwaretesting.com ROUTE_PREFIX=/# pytest tests/buoi4 -v
"""
import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.mark.regression
@pytest.mark.ui
def test_b4_a_add_to_cart_shows_a_toast(page):
    """Goal: user gets feedback after add-to-cart. Precondition: none. Expected: a toast appears."""
    product = HomePage(page).open().open_product("Combination Pliers").add_to_cart()
    expect(product.toast.first).to_have_text("Product added to shopping cart.")


@pytest.mark.regression
@pytest.mark.ui
def test_b4_b_cart_has_a_total(page):
    """Goal: cart shows prices. Precondition: one product, quantity 2. Expected: a positive total."""
    product = HomePage(page).open().open_product("Combination Pliers")
    unit_price = product.price()
    cart = product.add_to_cart(quantity=2).go_to_cart()
    expect(cart.product_titles.first).to_have_text("Combination Pliers")
    expect(cart.line_prices.first).to_be_visible()
    assert cart.line_totals()[0] == pytest.approx(unit_price * 2)
    assert cart.total_value() == pytest.approx(unit_price * 2)


@pytest.mark.regression
@pytest.mark.ui
def test_b4_c_search_without_results_counts_zero(page):
    """Goal: empty search state. Precondition: none. Expected: result counter says 0."""
    home = HomePage(page).open().search("zzz-no-such-tool")
    expect(home.search_result_count).to_contain_text("0")
    expect(home.no_results).to_have_text("There are no products found.")


@pytest.mark.regression
@pytest.mark.ui
def test_b4_d_login_empty_form_stays_on_login(page):
    """Goal: validation of the login form. Precondition: none. Expected: user stays on the login page."""
    login = LoginPage(page).open()
    login.submit_button.click()
    expect(page).to_have_url(re.compile(r"/auth/login$"))
    expect(login.email_error).to_have_text("Email is required")
    expect(login.password_error).to_have_text("Password is required")


@pytest.mark.regression
@pytest.mark.ui
def test_b4_e_header_has_contact_and_search(page):
    """Goal: header controls exist. Precondition: none. Expected: Contact link and Search button visible."""
    home = HomePage(page).open()
    expect(home.nav_contact).to_have_text("Contact")
    expect(home.search_button).to_have_text("Search")


@pytest.mark.regression
@pytest.mark.ui
def test_b4_f_home_lists_products(page, api):
    """Goal: catalogue is browsable. Precondition: none. Expected: products are listed."""
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    meta = api.get("/products", params={"page": 1}).json()
    if meta["total"] > meta["per_page"]:
        expect(home.pagination_next).to_be_visible()


@pytest.mark.regression
@pytest.mark.api
def test_b4_g_search_api_finds_wrench(api):
    """Goal: search endpoint answers. Precondition: none. Expected: results for 'wrench'."""
    names = [p["name"] for p in api.get("/products/search", params={"q": "wrench"}).json()["data"]]
    assert names and all("wrench" in n.lower() for n in names), names
