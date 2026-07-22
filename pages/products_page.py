from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class ProductsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.title: Locator = page.locator(
            "[data-test='title']"
        )
        self.inventory_items: Locator = page.locator(
            "[data-test='inventory-item']"
        )
        self.cart_link: Locator = page.locator(
            "[data-test='shopping-cart-link']"
        )
        self.sort_dropdown: Locator = page.locator(
            "[data-test='product-sort-container']"
        )

    def add_product_to_cart(
        self,
        product_name: str,
    ) -> None:
        product = self.inventory_items.filter(
            has_text=product_name
        )

        product.get_by_role(
            "button",
            name="Add to cart",
        ).click()

    def open_cart(self) -> None:
        self.cart_link.click()

    def sort_by(self, option: str) -> None:
        self.sort_dropdown.select_option(option)