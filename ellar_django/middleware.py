import typing as t

from ellar.common.types import ASGIApp, TMessage, TReceive, TScope, TSend
from starlette.datastructures import MutableHeaders


class DjangoAdminRedirectMiddleware:
    def __init__(self, app: ASGIApp, path_prefix: str) -> None:
        self.app = app
        self.path_prefix = path_prefix

    async def __call__(self, scope: TScope, receive: TReceive, send: TSend) -> t.Any:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def sender(message: TMessage) -> None:
            if message["type"] == "http.response.start":
                headers = message.get("headers")
                if headers:
                    working_headers = MutableHeaders(
                        raw=[
                            (key.decode("latin-1").lower().encode("latin-1"), value)
                            for key, value in headers
                        ]
                    )
                    location = working_headers.get("location")
                    if location and not location.startswith(self.path_prefix):
                        working_headers["Location"] = (
                            f"{self.path_prefix}{working_headers['Location']}"
                        )
                        message["headers"] = working_headers.raw
            await send(message)

        return await self.app(scope, receive, sender)
