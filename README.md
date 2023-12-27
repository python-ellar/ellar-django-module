<p align="center">
  <a href="#" target="blank"><img src="https://python-ellar.github.io/ellar/img/EllarLogoB.png" width="200" alt="Ellar Logo" /></a>
</p>
<p align="center">Ellar - Python ASGI web framework for building fast, efficient, and scalable RESTful APIs and server-side applications.</p>

![Test](https://github.com/python-ellar/ellar-django-module/actions/workflows/test_full.yml/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/python-ellar/ellar-django-module)
[![PyPI version](https://badge.fury.io/py/ellar-django-module.svg)](https://badge.fury.io/py/ellar-django-module)
[![PyPI version](https://img.shields.io/pypi/v/ellar-django-module.svg)](https://pypi.python.org/pypi/ellar-django-module)
[![PyPI version](https://img.shields.io/pypi/pyversions/ellar-django-module.svg)](https://pypi.python.org/pypi/ellar-django-module)

## Introduction
A simple way to add use Django ORM with Ellar

## Installation
```shell
pip install ellar-django-module
```

## Setup
If you are starting from scratch, then you need to scaffold a new project with ellar-cli as shown below:
```shell
ellar new my_project
```
Scaffolded project structure
```text
my_project/
├─ my_project/
│  ├─ apps/
│  ├─ core/
│  ├─ domain/
│  ├─ config.py
│  ├─ root_module.py
│  ├─ server.py
│  ├─ __init__.py
├─ tests/
├─ pyproject.toml
├─ README.md
```
After scaffolding our ellar application, we need to set up `DjangoModule` in `my_project/root_module.py`

```python
# my_project/root_module.py

from ellar.common import (
    Module,
    exception_handler,
    IExecutionContext,
    JSONResponse,
    Response,
)
from ellar.core import ModuleBase
from ellar.samples.modules import HomeModule
from ellar_django import DjangoModule


@Module(
    modules=[
        HomeModule,
        DjangoModule.setup(settings_module="my_project.config")
    ]
)
class ApplicationModule(ModuleBase):
    @exception_handler(404)
    def exception_404_handler(cls, ctx: IExecutionContext, exc: Exception) -> Response:
        return JSONResponse(dict(detail="Resource not found."))
```

The `DjangoModule` setup requires a string import of django `settings.py` or any file that contains django settings.
This is important for django models definitions and django admins views to work properly. But for now, we have used path to ellar config file to avoid some django errors.

It's also important to note that `DjangoModule` as added a wrapper around django cli tool. To verify this, still on your terminal, run the code below:
```shell
ellar django --help
```
This should show you the result below:
```shell
Usage: Ellar, Python Web framework django [OPTIONS]

  Ellar will always intercept and command with '--help'.

  So if you want to get help on any django command, simply wrap the command
  and --help in quotes

  For example: ellar django 'migrate --help'

Options:
  --help  Show this message and exit.
```
### Scaffolding Django Project
Now that django cli works, we need to scaffold a django project. why? 
Because we need `settings.py` and `url.py` provided by django `startproject` command but if you can create these files yourself and link them, 
then I don't think you need this section.

On the same terminal, run the command below:
```shell
ellar django startproject wsgi_django .
```
In the command above, we specified `.` as the current directory to avoid creating a nested directory.
Also, we need to delete `manage.py`, `wsgi.py`, `asgi.py` and leave only `settings.py` and `url.py`

Current project structure 
```text
my_project/
├─ my_project/
│  ├─ apps/
│  ├─ core/
│  ├─ domain/
│  ├─ config.py
│  ├─ root_module.py
│  ├─ server.py
│  ├─ __init__.py
├─ tests/
├─ wsgi_django/
│  ├─ settings.py
│  ├─ urls.py
│  ├─ __init__.py
├─ pyproject.toml
├─ README.md
```

### Update DjangoModuleSetup
Now, we have a `settings.py` with all required django settings in `wsgi_django.settings`. So lets apply that to `DjangoModule` setup.

```python
from ellar.common import (
    Module,
    exception_handler,
    IExecutionContext,
    JSONResponse,
    Response,
)
from ellar.core import ModuleBase
from ellar.samples.modules import HomeModule
from ellar_django import DjangoModule


@Module(
    modules=[
        HomeModule,
        DjangoModule.setup(settings_module="wsgi_django.settings", path_prefix='/-django-example')
    ]
)
class ApplicationModule(ModuleBase):
    @exception_handler(404)
    def exception_404_handler(cls, ctx: IExecutionContext, exc: Exception) -> Response:
        return JSONResponse(dict(detail="Resource not found."))
```
### Django Database Migration
It's about time to create some database. So as usual, we use django `migrate` command

```shell
ellar django migrate
```

Output:
```shell
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
```

### Start Server
Now, that we have everything setup, we can start the server
```shell
ellar runserver --reload
```
In the above example, we added `/-django-example` as path prefix. This is important because we need to group all django admin views 
with a prefix and also to avoid unnecessary `Page Not Found` errors.

We can visit [http://localhost:8000/-django-example/admin](http://localhost:8000/-django-example/admin) to see django Admin UI.

### Serving Django Static Files
If you visited the Django Admin view, you will notice the css and javascript files all returned 404 error.
To fix this we need to install `whitenoise` package.

```shell
pip install whitenoise
```

Afterward, we update the django settings with whitenoise middleware as shown blown
```python
...

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    ...
]
...
```
So when you visit [http://localhost:8000/-django-example/admin](http://localhost:8000/-django-example/admin) again, the page should be functional.

### Creating a Superuser
As you can see, we need to login to access the admin view. A quick way to do this is by creating
a superuser using `createsuperuser` command. So lets do this below:
```shell
ellar django createsuperuser
```
Follow the prompts and use the created credentials to log in to django admin panel.
