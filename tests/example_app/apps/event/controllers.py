"""
Define endpoints routes in python class-based fashion
example:

@Controller("/dogs", tag="Dogs", description="Dogs Resources")
class MyController(ControllerBase):
    @get('/')
    def index(self):
        return {'detail': "Welcome Dog's Resources"}
"""

import typing as t

from ellar.common import Controller, ControllerBase, get, post

from ...interfaces.events_repository import IEventRepository
from .schemas import EventSchema, EventSchemaOut


@Controller("/event")
class EventController(ControllerBase):
    def __init__(self, event_repo: IEventRepository):
        self.event_repo = event_repo

    @post("/", response={201: EventSchemaOut})
    def create_event(self, event: EventSchema):
        event = self.event_repo.create_event(**event.dict())
        return 201, event

    @get("/", response=t.List[EventSchema], name="event-list")
    def list_events(self):
        return list(self.event_repo.list_events())
