import typing as t
from abc import abstractmethod

if t.TYPE_CHECKING:
    from ..wsgi_django.db_models.models import Event


class IEventRepository:
    @abstractmethod
    def create_event(self, **kwargs: t.Dict) -> "Event":
        pass

    @abstractmethod
    def list_events(self) -> t.List["Event"]:
        pass
