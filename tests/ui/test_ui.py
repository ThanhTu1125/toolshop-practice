import pytest
from playwright.sync_api import expect

from pages.account_page import AccountPage
from pages.home_page import HomePage
from pages.login_page import LoginPage

pytestmark = pytest.mark.ui


# --- NHÓM 1: DANH SÁCH & TÌM KIẾM ---
def test_search_unknown_keyword_shows_no_results(page):
    """Goal: empty search results when searching with non-existent keyword.
    Precondition: none.
    Expected: 'There are no products found.' message and 0 product cards."""
    home = HomePage(page).open().search("zzz-no-such-tool")
    expect(home.no_results).to_have_text("There are no products found.")
    expect(home.product_names).to_have_count(0)


@pytest.mark.parametrize("order", ["price,asc", "price,desc"])
def test_sort_by_price_orders_products(page, order):
    """Goal: sorting products by price.
    Precondition: none.
    Expected: prices on the first page are sorted in the chosen order."""
    home = HomePage(page).open().sort_by(order)
    expect(home.sorting_completed).to_be_visible()
    prices = home.prices()
    assert prices, "No product prices found"
    assert prices == sorted(prices, reverse=("desc" in order))


# --- NHÓM 2: BỘ LỌC ---
def test_filter_by_hammer_category(page):
    """Goal: filtering products by category checkbox.
    Precondition: none.
    Expected: only hammer products are displayed after filter."""
    home = HomePage(page).open().filter_by_category("Hammer")
    expect(home.filter_completed).to_be_visible()
    names = home.product_names.all_inner_texts()
    assert names, "No products displayed after filtering"
    assert all("hammer" in n.lower() for n in names), names


# --- NHÓM 3: CHI TIẾT SẢN PHẨM ---
def test_product_detail_displays_correct_name_and_price(page):
    """Goal: opening a product displays matching title and unit price.
    Precondition: Claw Hammer exists on home page.
    Expected: detail page shows Claw Hammer title and price > 0."""
    product = HomePage(page).open().open_product("Claw Hammer")
    expect(product.name).to_contain_text("Claw Hammer")
    assert product.price() > 0


# --- NHÓM 4: GIỎ HÀNG ---
def test_cart_line_price_equals_unit_price_times_quantity(page):
    """Goal: cart line price calculation.
    Precondition: fresh cart per test context.
    Expected: line price equals unit price times quantity."""
    product = HomePage(page).open().open_product("Claw Hammer")
    unit_price = product.price()
    product.add_to_cart(quantity=2)
    expect(product.cart_quantity).to_have_text("2")
    cart = product.go_to_cart()
    expect(cart.line_prices.first).to_be_visible()
    assert cart.line_totals()[0] == pytest.approx(unit_price * 2)


def test_cart_continue_shopping_returns_to_home(page):
    """Goal: continue shopping button navigates back to product grid.
    Precondition: product added to cart.
    Expected: home page product grid is visible again."""
    product = HomePage(page).open().open_product("Claw Hammer")
    product.add_to_cart(quantity=1)
    expect(product.cart_quantity).to_have_text("1")
    cart = product.go_to_cart()
    home = cart.click_continue_shopping()
    expect(home.product_names.first).to_be_visible()


# --- NHÓM 5: XÁC THỰC ---
def test_login_empty_form_shows_required_errors(page):
    """Goal: client-side form validation on login.
    Precondition: none.
    Expected: error messages for both email and password."""
    login = LoginPage(page).open().submit()
    expect(login.email_error).to_contain_text("Email is required")
    expect(login.password_error).to_contain_text("Password is required")


# --- NHÓM 6: LIÊN HỆ & TÀI KHOẢN ---
def test_account_page_with_session_storage_shows_user_menu(logged_in_page):
    """Goal: access account with pre-authenticated storage state.
    Precondition: session storage state created by conftest.py.
    Expected: My account page opens and user menu displays QA Bot."""
    account = AccountPage(logged_in_page).open()
    expect(account.title).to_have_text("My account")
    expect(account.nav_menu).to_contain_text("QA Bot")
