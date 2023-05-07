import abc

from cleo.io.io import IO
from poetry.poetry import Poetry


class IHandler(abc.ABC):
    @abc.abstractmethod
    def handle(self, poetry: Poetry, io: IO) -> None:
        raise NotImplementedError
