import os

from django.core.asgi import get_asgi_application
from ellar.common import IModuleSetup, Module, ModuleRouter
from ellar.core import DynamicModule, Request
from ellar.core.router_builders import ModuleRouterBuilder
from starlette.responses import RedirectResponse
from starlette.routing import Mount

from .commands import django_command_wrapper

_router = ModuleRouter()


@_router.get("/")
async def _redirect_route(req: Request) -> RedirectResponse:
    return RedirectResponse(url=str(req.base_url))


@Module(commands=[django_command_wrapper])
class DjangoModule(IModuleSetup):
    @classmethod
    def setup(cls, settings_module: str, path_prefix: str = "/dj") -> "DynamicModule":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
        _router_as_mount = ModuleRouterBuilder.build(_router)

        mount = Mount(
            path_prefix,
            routes=[
                _router_as_mount,
                Mount("/", app=get_asgi_application()),
            ],
        )
        return DynamicModule(cls, routers=[mount])
