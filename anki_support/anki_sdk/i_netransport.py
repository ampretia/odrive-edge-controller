from abc import ABC, abstractmethod


class ITransport(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def send_position(self,data):
        pass