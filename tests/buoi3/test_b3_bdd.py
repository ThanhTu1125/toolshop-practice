"""Buoi 3 - BDD with pytest-bdd. Step definitions only call page objects (no new locators here).

Run:  pytest tests/buoi3 -v
Each Examples row becomes its own pytest test - read the test names in the output.
"""
import pytest
from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from pages.home_page import HomePage

pytestmark = [pytest.mark.bdd, pytest.mark.ui]

# Paths are relative to bdd_features_base_dir in pytest.ini (tests/buoi3/features)
# TODO B3.4: add "cart.feature" here once you have written it
scenarios("search.feature", "cart.feature")


# ---------------------------------------------------------------- given (B3.1: read and run)
@given("I am on the home page", target_fixture="home")
def home(page):
    home = HomePage(page).open()
    expect(home.product_names.first).to_be_visible()
    return home


@when(parsers.parse('I search for "{keyword}"'))
def search(home, keyword):
    home.search(keyword)


@then(parsers.parse('every product name contains "{keyword}"'))
def names_contain(home, keyword):
    expect(home.search_completed).to_be_visible()
    names = home.product_names.all_inner_texts()
    assert names and all(keyword.lower() in n.lower() for n in names), names


# ---------------------------------------------------------------- B3.2: the two missing steps
# Run pytest first: pytest-bdd tells you exactly which step text has no definition.
@then(parsers.parse('the search caption mentions "{keyword}"'))
def caption_mentions(home, keyword):
    expect(home.search_caption).to_contain_text(keyword)


@then(parsers.parse('I see the message "{message}"'))
def see_message(home, message):
    expect(home.no_results).to_have_text(message)


# ---------------------------------------------------------------- B3.4: steps for cart.feature
# Hints:
#   - "When I open the product ..." returns a ProductPage: use target_fixture="product_page"
#   - read the unit price BEFORE adding to the cart and keep it: target_fixture="unit_price"
#   - numbers in steps: parsers.parse("... quantity {quantity:d}")


@when(parsers.parse('I open the product "{product}"'), target_fixture="product_page")
def open_product(home, product):
    return home.open_product(product)


@when(parsers.parse("I add it to the cart with quantity {quantity:d}"), target_fixture="unit_price")
def add_to_cart(product_page, quantity):
    unit = product_page.price()  # đọc giá trước khi thêm
    product_page.add_to_cart(quantity=quantity)
    expect(product_page.cart_quantity).to_have_text(str(quantity))
    return unit


@when("I open the cart", target_fixture="cart")
def open_cart(product_page):
    return product_page.go_to_cart()


@then(parsers.parse('the cart contains "{product}"'))
def cart_contains(cart, product):
    expect(cart.product_titles).to_have_count(1)
    expect(cart.product_titles.first).to_have_text(product)


@then(parsers.parse("the line price equals the unit price times {quantity:d}"))
def line_price_equals(cart, unit_price, quantity):
    assert cart.line_totals()[0] == pytest.approx(unit_price * quantity)


@then("the cart total equals the sum of the line prices")
def cart_total_equals(cart):
    assert cart.total_value() == pytest.approx(sum(cart.line_totals()))
