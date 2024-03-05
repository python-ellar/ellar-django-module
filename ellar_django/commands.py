import sys

import click

HELP_MESSAGE = """
Ellar will always intercept and command with '--help'.

So if you want to get help on any django command,
simply wrap the command and --help in quotes

For example: ellar django 'migrate --help' or python manage.py django 'migrate --help'
"""


@click.command(
    name="django",
    context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
    help=HELP_MESSAGE,
)
def django_command_wrapper() -> None:
    from django.core.management import execute_from_command_line

    args = []
    skip = 1

    if "manage.py" in sys.argv:  # pragma: no cover
        skip = 2

    for item in sys.argv[skip:]:
        args.extend(item.split(" "))
    execute_from_command_line(args)
