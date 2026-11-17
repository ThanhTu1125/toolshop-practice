from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/auth/login"

    def __init__(self, page):
        super().__init__(page)
        self.email = page.get_by_test_id("email")
        self.password = page.get_by_test_id("password")
        self.submit_button = page.get_by_test_id("login-submit")
        self.error = page.get_by_test_id("login-error")
        self.email_error = page.get_by_test_id("email-error")
        self.password_error = page.get_by_test_id("password-error")

    def submit(self):
        self.submit_button.click()
        return self

    def login(self, email: str = "", password: str = ""):
        if email:
            self.email.fill(email)
        if password:
            self.password.fill(password)
        return self.submit()
