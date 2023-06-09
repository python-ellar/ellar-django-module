import pytest


@pytest.mark.django_db
def test_admin_route_works(client):
    res = client.get("/dj/admin", follow_redirects=True)
    assert res.status_code == 200
    assert "Log in | Django site admin" in res.text
