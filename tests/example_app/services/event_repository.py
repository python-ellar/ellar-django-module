import typing as t
from datetime import datetime, timedelta

from ellar.di import injectable

from ..interfaces.events_repository import IEventRepository
from ..wsgi_django.db_models.models import Event


@injectable
class EventRepository(IEventRepository):
    _dummy_data = dict(
        title="TestEvent1Title",
        start_date=str(datetime.now().date()),
        end_date=str((datetime.now() + timedelta(days=5)).date()),
    )

    def create_dummy_events(self):
        for i in range(3):
            object_data = self._dummy_data.copy()
            object_data.update(title=f"{object_data['title']}_{i + 1}")
            Event.objects.create(**object_data)
        print("Done")

    def create_event(self, **kwargs: t.Dict) -> "Event":
        return Event.objects.create(**kwargs)

    def list_events(self) -> t.List["Event"]:
        self.create_dummy_events()
        return Event.objects.all()
