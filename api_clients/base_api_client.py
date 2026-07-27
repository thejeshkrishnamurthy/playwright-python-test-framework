from typing import Any

from playwright.sync_api import (
    APIRequestContext,
    APIResponse,
)

from utils.logger import get_logger


class BaseApiClient:
    def __init__(
        self,
        api_context: APIRequestContext,
    ) -> None:
        self.api_context = api_context
        self.logger = get_logger(self.__class__.__name__)

    def get(
        self,
        path: str,
        **kwargs: Any,
    ) -> APIResponse:
        self.logger.info("GET %s", path)
        return self.api_context.get(path, **kwargs)

    def post(
        self,
        path: str,
        **kwargs: Any,
    ) -> APIResponse:
        self.logger.info("POST %s", path)
        return self.api_context.post(path, **kwargs)

    def put(
        self,
        path: str,
        **kwargs: Any,
    ) -> APIResponse:
        self.logger.info("PUT %s", path)
        return self.api_context.put(path, **kwargs)

    def patch(
        self,
        path: str,
        **kwargs: Any,
    ) -> APIResponse:
        self.logger.info("PATCH %s", path)
        return self.api_context.patch(path, **kwargs)

    def delete(
        self,
        path: str,
        **kwargs: Any,
    ) -> APIResponse:
        self.logger.info("DELETE %s", path)
        return self.api_context.delete(
            path,
            **kwargs,
        )
