import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from ellar.common.constants import MODULE_METADATA
from ellar.reflect import reflect

from ellar_django.module import DjangoModule, _default_blacklisted_commands

HELP_OUTPUT = """Usage: django [OPTIONS] COMMAND [ARGS]...

  Ellar Django Commands

Options:
  -v, --version  Show the version and exit.
  --help         Show this message and exit.

Commands:
"""


def test_command_succeeds() -> None:
    call_command("check")


def test_nonexistent_command_fails() -> None:
    with pytest.raises(CommandError, match="Unknown command"):
        call_command("nonexistent_command")


def test_command_help(cli_runner):
    with reflect.context():
        DjangoModule.setup(
            settings_module="example_app.wsgi_django.settings"
        ).apply_configuration()
        django_command_group = reflect.get_metadata(
            MODULE_METADATA.COMMANDS, DjangoModule
        )[0]

        res = cli_runner.invoke(django_command_group, ["--help"])
        assert res.exit_code == 0
        assert HELP_OUTPUT in res.stdout


def test_check_help(cli_runner):
    with reflect.context():
        DjangoModule.setup(
            settings_module="example_app.wsgi_django.settings"
        ).apply_configuration()
        django_command_group = reflect.get_metadata(
            MODULE_METADATA.COMMANDS, DjangoModule
        )[0]

        res = cli_runner.invoke(django_command_group, ["check", "--help"])
        assert res.exit_code == 0
        assert (
            "usage: manage.py check [-h] [--tag TAGS] [--list-tags] [--deploy]"
            in res.stdout
        )


@pytest.mark.parametrize("command_name", list(_default_blacklisted_commands))
def test_default_blacklist_command(cli_runner, command_name):
    with reflect.context():
        DjangoModule.setup(
            settings_module="example_app.wsgi_django.settings"
        ).apply_configuration()
        django_command_group = reflect.get_metadata(
            MODULE_METADATA.COMMANDS, DjangoModule
        )[0]

        res = cli_runner.invoke(django_command_group, [command_name])
        assert res.exit_code == 2
        assert f"Error: No such command '{command_name}'" in res.stdout


def test_django_version(cli_runner):
    with reflect.context():
        DjangoModule.setup(
            settings_module="example_app.wsgi_django.settings"
        ).apply_configuration()
        django_command_group = reflect.get_metadata(
            MODULE_METADATA.COMMANDS, DjangoModule
        )[0]

        res = cli_runner.invoke(django_command_group, ["-v"])
        assert res.exit_code == 0
        assert "Django Version: " in res.stdout


def test_collect_static_version(cli_runner):
    with reflect.context():
        DjangoModule.setup(
            settings_module="example_app.wsgi_django.settings"
        ).apply_configuration()
        django_command_group = reflect.get_metadata(
            MODULE_METADATA.COMMANDS, DjangoModule
        )[0]

        res = cli_runner.invoke(django_command_group, ["check", "db_models"])
        assert res.exit_code == 0
        assert res.stdout == "System check identified no issues (0 silenced).\n"
