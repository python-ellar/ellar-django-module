from ellar.common import (
    IExecutionContext,
    JSONResponse,
    Module,
    Response,
    exception_handler,
)
from ellar.core import ModuleBase
from ellar.di import ProviderConfig

from ellar_django import DjangoModule

from .apps.event.module import EventModule
from .interfaces.events_repository import IEventRepository


@Module(
    modules=[
        DjangoModule.setup(settings_module="ellar_and_django_orm.wsgi_django.settings"),
        EventModule,
    ],
    providers=[
        ProviderConfig(IEventRepository, use_class="ellar_and_django_orm.services.event_repository:EventRepository")
    ],
)
class ApplicationModule(ModuleBase):
    @exception_handler(404)
    def exception_404_handler(cls, ctx: IExecutionContext, exc: Exception) -> Response:
        return JSONResponse({"detail": "Resource not found."}, status_code=404)
