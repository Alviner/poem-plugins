import abc

from poetry.plugins.application_plugin import ApplicationPlugin


class BasePlugin(ApplicationPlugin, abc.ABC):
    pass
