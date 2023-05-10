from dataclasses import dataclass
from typing import Any, Mapping

from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.event import Event
from cleo.events.event_dispatcher import EventDispatcher
from poetry.console.commands.build import BuildCommand
from poetry.poetry import Poetry

from poem_plugins.config import VersionConfig
from poem_plugins.dispatchers.base import BaseDispatcher
from poem_plugins.handlers.version import VersionHandler


@dataclass(frozen=True)
class VersionDispatcher(BaseDispatcher):
    @classmethod
    def factory(cls) -> "VersionDispatcher":
        return cls()

    def get_raw_config(self, poetry: Poetry) -> Mapping[str, Any]:
        base_raw_config = super().get_raw_config(poetry)
        return base_raw_config.get("version", {})

    def get_config(self, poetry: Poetry) -> VersionConfig:
        base = self.get_raw_config(poetry)
        return VersionConfig.fabric(base)

    def __call__(
        self,
        event: Event,
        event_name: str,
        dispatcher: EventDispatcher,
    ) -> None:
        if not isinstance(event, ConsoleCommandEvent):
            return
        command = event.command
        if not isinstance(command, BuildCommand):
            return
        io = event.io
        poetry = command.poetry
        try:
            config = self.get_config(poetry)
        except Exception as exc:
            io.write_error_line(
                "<b>poem-plugins</b>: "
                f"Cannot load version config, skipping: {exc}",
            )
            return

        handler = VersionHandler.factory(config)
        handler.handle(poetry, io)
