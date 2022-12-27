import abc

from poem_plugins.general.versions import Version


class IVervsionDriver(abc.ABC):
    @abc.abstractmethod
    def get_version(self, git_version_prefix: str = "v") -> Version:
        raise NotImplementedError
