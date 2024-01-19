from abc import ABC, abstractmethod
from .events import IObserver


class ICar(ABC):

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    async def send_command(self, command: bytes) -> None:
        pass

    @abstractmethod
    async def start_notify(self, observer: IObserver) -> None:
        pass
