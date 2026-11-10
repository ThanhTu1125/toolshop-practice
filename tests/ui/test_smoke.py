import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.contact_page import ContactPage


@pytest.mark.smoke
def test_smoke_search_contains_pliers(page):
    """Tìm pliers: mọi tên sản phẩm chứa 'pliers'"""
    home = HomePage(page).open().search("pliers")
    
    # Chờ quá trình tìm kiếm hoàn tất
    expect(home.search_completed).to_be_visible()
    
    # Lấy danh sách tên sản phẩm và kiểm tra
    names = home.product_names.all_inner_texts()
    assert len(names) > 0, "Không tìm thấy sản phẩm nào"
    assert all("pliers" in name.lower() for name in names), "Có sản phẩm không chứa chữ 'pliers'"


@pytest.mark.smoke
def test_smoke_add_to_cart_updates_badge(page):
    """Mở 'Claw Hammer', thêm số lượng 3: badge giỏ hàng hiện 3"""
    product = HomePage(page).open().open_product("Claw Hammer")
    product.add_to_cart(quantity=3)
    
    # Kiểm tra số lượng trên biểu tượng giỏ hàng
    expect(product.cart_quantity).to_have_text("3")


@pytest.mark.smoke
def test_smoke_login_wrong_password_shows_error(page):
    """Đăng nhập bằng email không tồn tại: 'Invalid email or password'"""
    login_page = LoginPage(page).open()
    
    # Dùng email ảo để tránh bị khoá tài khoản dùng chung của lớp
    login_page.login("nobody-here@example.com", "Wrong-Password-123")
    
    # Kiểm tra thông báo lỗi và URL
    expect(login_page.error).to_contain_text("Invalid email or password")
    expect(page).to_have_url(re.compile(r"/auth/login$"))


@pytest.mark.smoke
def test_smoke_contact_empty_form_shows_errors(page):
    """Bấm Send ở form Liên hệ để trống: 'Subject is required' và 'Message is required'"""
    contact_page = ContactPage(page).open()
    contact_page.submit()
    
    # ContactPage đã gom sẵn các lỗi vào locator self.errors
    expect(contact_page.errors.filter(has_text="Subject is required")).to_be_visible()
    expect(contact_page.errors.filter(has_text="Message is required")).to_be_visible()