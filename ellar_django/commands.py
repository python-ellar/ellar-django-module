import sys
import typing as t

import django
import ellar_cli.click as click


class _CommandItem(t.NamedTuple):
    name: str
    description: str


_django_support_commands: t.List[_CommandItem] = [
    _CommandItem(
        name="migrate",
        description="Synchronizes the database state with the current set of models and migrations",
    ),
    _CommandItem(
        name="makemigrations",
        description="Creates new migrations based on the changes detected to your models.",
    ),
    _CommandItem(
        name="check",
        description="inspects the entire Django project for common problems",
    ),
    _CommandItem(
        name="createcachetable",
        description="Creates the cache tables for use with the database cache backend",
    ),
    _CommandItem(
        name="dbshell",
        description="Runs the command-line client for the database engine",
    ),
    _CommandItem(
        name="diffsettings",
        description="Displays differences between the current settings and default settings",
    ),
    _CommandItem(
        name="dumpdata",
        description="Outputs to standard output all data in the database",
    ),
    _CommandItem(
        name="flush",
        description="Removes all data from the database and re-executes any post-synchronization handlers",
    ),
    _CommandItem(
        name="inspectdb", description="Introspects the database tables in the database"
    ),
    _CommandItem(
        name="loaddata",
        description="Searches for and loads the contents into the database.",
    ),
    _CommandItem(
        name="optimizemigration",
        description="Optimizes the operations for the named migration and overrides the existing file",
    ),
    _CommandItem(
        name="showmigrations", description="Shows all migrations in a project."
    ),
    _CommandItem(
        name="sqlflush",
        description="Prints the SQL statements that would be executed for the flush command",
    ),
    _CommandItem(
        name="sqlmigrate", description="Prints the SQL for the named migration."
    ),
    _CommandItem(
        name="sqlsequencereset",
        description="Prints the SQL statements for resetting sequences for the given app name(s)",
    ),
    _CommandItem(
        name="squashmigrations", description="Squashes the migrations for app_label"
    ),
    _CommandItem(
        name="startapp", description="Creates a Django app directory structure"
    ),
    _CommandItem(
        name="changepassword",
        description="This command is only available if Django’s authentication system",
    ),
    _CommandItem(
        name="createsuperuser",
        description="Creates a superuser account (a user who has all permissions)",
    ),
    _CommandItem(
        name="collectstatic", description="Expose static files to STATIC_ROOT folder"
    ),
    _CommandItem(name="findstatic", description="Search for a static file location"),
    _CommandItem(
        name="clearsessions",
        description="Can be run as a cron job or directly to clean out expired sessions.",
    ),
]


def version_callback(ctx: click.Context, _: t.Any, value: bool) -> None:
    if value:
        click.echo(f"Django Version: {django.__version__}")
        raise click.Exit(0)


@click.group(
    name="django",
    help="- Ellar Django Commands",
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


def _add_django_command(command_item: _CommandItem) -> None:
    def help_callback(ctx: click.Context, _: t.Any, value: bool) -> None:
        from django.core.management import execute_from_command_line

        if value:
            args = ["manage.py", command_item.name, "--help"]

            execute_from_command_line(args)
            raise click.Exit(0)

    @django_command.command(
        name=command_item.name,
        help=command_item.description,
        context_settings={"ignore_unknown_options": True, "allow_extra_args": True},
        add_help_option=False,
    )
    @click.option(
        "-h",
        "--help",
        callback=help_callback,
        help="Show the version and exit.",
        is_flag=True,
        expose_value=False,
        is_eager=True,
    )
    @click.with_app_context
    def _command() -> None:
        from django.core.management import execute_from_command_line

        args = ["manage.py", command_item.name]

        for item in sys.argv[3:]:
            args.extend(item.split(" "))
        execute_from_command_line(args)


list(map(_add_django_command, _django_support_commands))
