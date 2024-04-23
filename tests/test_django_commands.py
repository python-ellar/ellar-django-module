import pytest
from django.core.management import call_command
from django.core.management.base import CommandError


def test_command_succeeds() -> None:
    call_command("check")


def test_nonexistent_command_fails() -> None:
    with pytest.raises(CommandError, match="Unknown command"):
        call_command("nonexistent_command")
