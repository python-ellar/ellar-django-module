import click.testing
import pytest
from django.contrib.auth import get_user_model
from ellar.testing import Test
from example_app.root_module import ApplicationModule

test_module = Test.create_test_module(modules=[ApplicationModule])
test_module.create_application()
# test_module.create_application()  is very important if there are things that requires django settings.
# In my case, `user_model = get_user_model()`

user_model = get_user_model()


@pytest.fixture()
def admin_user():
    return user_model.object.create_superuser(
        username="ellar", email="ellar@example.com", password="password"
    )


@pytest.fixture()
def client():
    with test_module.get_test_client() as _client:
        yield _client


@pytest.fixture
def cli_runner():
    return click.testing.CliRunner()
