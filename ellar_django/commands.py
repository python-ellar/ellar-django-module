import sys

from ellar.common.commands import command

HELP_MESSAGE = """
Ellar will always intercept and command with '--help'.

So if you want to get help on any django command,
simply wrap the command and --help in quotes

For example: ellar django 'migrate --help'
"""


@command(
    name="django",
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True),
    help=HELP_MESSAGE,
)
def django_command_wrapper() -> None:
    from django.core.management import execute_from_command_line

    args = []
    for item in sys.argv[1:]:
        args.extend(item.split(" "))
    execute_from_command_line(args)
