import time
import pytest
from playwright.sync_api import expect

# AI generated test draft (flawed: hard-coded URL, sleep, direct locators, loose assertion)
def test_contact_form_without_subject(page):
    page.goto("https://practicesoftwaretesting.com/contact")
    page.get_by_test_id("first-name").fill("John")
    page.get_by_test_id("last-name").fill("Doe")
    page.get_by_test_id("email").fill("john@example.com")
    page.get_by_test_id("message").fill("Hello, this is a test message with enough length.")
    time.sleep(1)
    page.get_by_test_id("contact-submit").click()
    expect(page.get_by_test_id("subject-error")).to_be_visible()
