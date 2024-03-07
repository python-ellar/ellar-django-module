import pytest


@pytest.mark.django_db
def test_admin_route_works(client):
    res = client.get("/dj/admin", follow_redirects=True)
    assert res.status_code == 200
    assert "admin/css/login.css" in res.text
