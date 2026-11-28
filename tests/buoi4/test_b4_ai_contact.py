"""Buoi 4 - Exercise B4.6: AI generated test, human reviewed and corrected.

Review findings:
- Locator: Removed direct page locators, replaced with ContactPage page object methods.
- URLs: Removed hard-coded URL, uses ContactPage.open().
- Waiting: Removed time.sleep(1), relying on Playwright web-first assertions.
- Assertion: Replaced loose to_be_visible() with strict to_have_text("Subject is required").
- Challenge test: Added non-empty attachment test asserting "File should be empty."
"""
from pathlib import Path
import pytest
from playwright.sync_api import expect

from pages.contact_page import ContactPage


@pytest.mark.regression
@pytest.mark.ui
def test_contact_form_without_subject_shows_error(page):
    """Goal: validate contact form subject requirement.
    Precondition: user fills required fields except subject.
    Expected: error 'Subject is required' is displayed."""
    contact = ContactPage(page).open()
    contact.first_name.fill("John")
    contact.last_name.fill("Doe")
    contact.email.fill("john.doe@example.com")
    contact.message.fill("Hello, this is a test inquiry with sufficient character length.")
    contact.submit()
    expect(contact.subject_error).to_have_text("Subject is required")


@pytest.mark.regression
@pytest.mark.ui
def test_contact_form_non_empty_attachment_shows_error(page, tmp_path: Path):
    """Goal: validate file attachment rule (Toolshop only accepts 0-byte empty files).
    Precondition: user attaches a non-empty file.
    Expected: error 'File should be empty.' is displayed."""
    test_file = tmp_path / "sample.txt"
    test_file.write_text("Non-empty content", encoding="utf-8")

    contact = ContactPage(page).open()
    contact.first_name.fill("John")
    contact.last_name.fill("Doe")
    contact.email.fill("john.doe@example.com")
    contact.subject.select_option("customer-service")
    contact.message.fill("Hello, this is a test message with an attachment.")
    contact.attach(str(test_file))
    contact.submit()
    expect(contact.attachment_error).to_have_text("File should be empty.")
