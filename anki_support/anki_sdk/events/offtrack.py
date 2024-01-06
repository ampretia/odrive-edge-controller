from .abstractevent import Event
import struct


class OffTrack(Event):

    def __init__(self):
        pass

    def build(self):
        return self


    def __str__(self):
        return f"Off Track !!!"

    def __repr__(self):
        return self.__str__()