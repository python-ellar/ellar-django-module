import os
import typing as t

from django.core.asgi import get_asgi_application
from ellar.common import IModuleSetup, Module, ModuleRouter
from ellar.core import DynamicModule, Request
from ellar.core.router_builders import ModuleRouterBuilder
from starlette.responses import RedirectResponse
from starlette.routing import Mount

from ellar_django.commands import get_django_command

from .middleware import DjangoAdminRedirectMiddleware

_router = ModuleRouter()
_default_blacklisted_commands: t.Set[str] = {
    "runserver",
    "startapp",
    "startproject",
}


@_router.get("/")
async def _redirect_route(req: Request) -> RedirectResponse:
    return RedirectResponse(url=str(req.base_url))


@Module()
class DjangoModule(IModuleSetup):
    @classmethod
    def setup(
        cls,
        settings_module: str,
        path_prefix: str = "/dj",
        command_blacklist: t.Optional[t.Set[str]] = None,
    ) -> "DynamicModule":
        blacklisted_commands = set(
            list(_default_blacklisted_commands) + list(command_blacklist or set())
        )

        assert path_prefix not in [
            "",
            "/",
        ], "Invalid path prefix, please set a valid path prefix"

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
        _router_as_mount = ModuleRouterBuilder.build(_router)

        mount = Mount(
            path_prefix,
            routes=[
                _router_as_mount,
                Mount(
                    "/",
                    app=DjangoAdminRedirectMiddleware(
                        get_asgi_application(), path_prefix
                    ),
                ),
            ],
        )

        return DynamicModule(
            cls, routers=[mount], commands=[get_django_command(blacklisted_commands)]
        )
