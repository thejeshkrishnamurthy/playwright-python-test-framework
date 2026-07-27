from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.username_input: Locator = page.get_by_placeholder("Username")
        self.password_input: Locator = page.get_by_placeholder("Password")
        self.login_button: Locator = page.get_by_role(
            "button",
            name="Login",
        )
        self.error_message: Locator = page.locator("[data-test='error']")

    def open(self) -> None:
        self.navigate("/")

    def login(
        self,
        username: str,
        password: str,
    ) -> None:
        self.logger.info("Logging in as user: %s", username)

        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
