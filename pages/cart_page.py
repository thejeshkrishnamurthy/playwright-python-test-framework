from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.cart_items: Locator = page.locator("[data-test='inventory-item']")
        self.checkout_button: Locator = page.get_by_role(
            "button",
            name="Checkout",
        )

    def checkout(self) -> None:
        self.checkout_button.click()

    def product(self, product_name: str) -> Locator:
        return self.cart_items.filter(has_text=product_name)
