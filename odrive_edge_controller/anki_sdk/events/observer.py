from abc import ABC, abstractmethod

# from .subject import ISubject


class IObserver(ABC):
    @abstractmethod
    async def update(self, event) -> None:
        pass
