import json
from datetime import datetime, timedelta

import pytest
from example_app.apps.event.schemas import EventSchema
from example_app.wsgi_django.db_models.models import Event


@pytest.mark.django_db
class TestEventController:
    def test_create_event_works(self, client):
        response = client.post(
            "/event/",
            json={
                "title": "TestEvent1Title",
                "start_date": str(datetime.now().date()),
                "end_date": str((datetime.now() + timedelta(days=5)).date()),
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert Event.objects.filter(pk=data.get("id")).exists()

    def test_list_events_works(self, client):
        response = client.get("/event/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 4
        event_schema = [
            json.loads(EventSchema.from_orm(item).json())
            for item in Event.objects.all()
        ]
        assert event_schema == data
