from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.first_name: Locator = page.locator(
            "[data-test='firstName']"
        )
        self.last_name: Locator = page.locator(
            "[data-test='lastName']"
        )
        self.postal_code: Locator = page.locator(
            "[data-test='postalCode']"
        )
        self.continue_button: Locator = page.get_by_role(
            "button",
            name="Continue",
        )
        self.finish_button: Locator = page.get_by_role(
            "button",
            name="Finish",
        )
        self.confirmation_header: Locator = page.locator(
            "[data-test='complete-header']"
        )

    def enter_customer_details(
        self,
        first_name: str,
        last_name: str,
        postal_code: str,
    ) -> None:
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)
        self.continue_button.click()

    def finish_order(self) -> None:
        self.finish_button.click()