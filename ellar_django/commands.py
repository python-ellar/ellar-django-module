import typing as t

import django
import ellar_cli.click as click
from django.core.management import get_commands, load_command_class


class _CommandItem(t.NamedTuple):
    name: str
    description: str


def get_command_description(command_name: str) -> str:
    module = get_commands()[command_name]
    CommandClass = load_command_class(module, command_name)
    CommandClass.help = f"[{module.split('.')[0]}] {CommandClass.help}"
    return CommandClass.help


def _generate_command_list(
    blacklist_commands: t.Set[str],
) -> t.Generator[_CommandItem, None, None]:
    commands = get_commands()
    for command in commands:
        if command in blacklist_commands:
            continue
        description = get_command_description(command)
        yield _CommandItem(name=command, description=description)


def version_callback(ctx: click.Context, _: click.Parameter, value: bool) -> None:
    if value:
        click.echo(f"Django Version: {django.__version__}")
        ctx.exit()


def show_help_callback(ctx: click.Context, _: click.Parameter, value: bool) -> None:
    if value:
        command_args = ["manage.py", ctx.info_name, "--help"]
        django.core.management.execute_from_command_line(command_args)


def _add_django_command(
    django_command: click.Group, command_item: _CommandItem
) -> None:
    @django_command.command(
        name=command_item.name,
        help=command_item.description,
        context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
        add_help_option=False,
    )
    @click.option(
        "-h",
        "--help",
        callback=show_help_callback,
        help="Show the command help.",
        is_flag=True,
        expose_value=False,
        is_eager=True,
    )
    @click.pass_context
    def command(
        ctx: click.Context, *args: t.Tuple[t.Any, ...], **kwargs: t.Dict[str, t.Any]
    ) -> None:
        command_args = ["manage.py", command_item.name] + list(ctx.args)
        django.core.management.execute_from_command_line(command_args)


def get_django_command(blacklisted_commands: t.Set[str]) -> click.Group:
    @click.group(
        name="django",
        help="Ellar Django Commands",
    )
    @click.option(
        "-v",
        "--version",
        callback=version_callback,
        help="Show the version and exit.",
        is_flag=True,
        expose_value=False,
        is_eager=True,
    )
    @click.pass_context
    def django_command(ctx: click.Context) -> None:
        pass

    for command_item in _generate_command_list(blacklisted_commands):
        _add_django_command(
            django_command=t.cast(click.Group, django_command),
            command_item=command_item,
        )

    return t.cast(click.Group, django_command)
