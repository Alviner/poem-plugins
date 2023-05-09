from cleo.events.console_events import COMMAND
from poetry.console.application import Application

from poem_plugins.dispatchers.version import VersionDispatcher
from poem_plugins.plugins.base import BasePlugin


class VersionPlugin(BasePlugin):
    def activate(self, application: Application) -> None:
        if not application.event_dispatcher:
            return

        version_dispatcher = VersionDispatcher.factory()
        application.event_dispatcher.add_listener(
            COMMAND,
            version_dispatcher,
        )
