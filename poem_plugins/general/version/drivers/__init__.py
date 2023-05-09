import abc

from poem_plugins.general.version import Version


class IVersionDriver(abc.ABC):
    @abc.abstractmethod
    def get_version(self) -> Version:
        raise NotImplementedError

    @abc.abstractmethod
    def render_version_file(
        self,
        version: Version,
    ) -> str:
        raise NotImplementedError
