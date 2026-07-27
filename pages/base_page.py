from playwright.sync_api import Page

from utils.config import get_settings
from utils.logger import get_logger


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.settings = get_settings()
        self.logger = get_logger(self.__class__.__name__)

    def navigate(self, path: str = "/") -> None:
        self.logger.info("Navigating to path: %s", path)
        self.page.goto(path)
        self.page.wait_for_load_state("domcontentloaded")

    def current_url(self) -> str:
        return self.page.url
