from anki_support.anki_sdk.track.layout import Layout
from .events import LocalizationPosition, LocalizationTransition
from .car_interface import ICar


class CarPosition:
    def __init__(self, layout: Layout, car: ICar, piece=None):
        self.layout = layout
        self.current = piece
        self.name = car.get_name()
        self.location = -1
        self.linearOffset = 0

    def set_finish(self):
        self.current = self.layout.get_finish()

    def transistion(self, transitionEvt: LocalizationTransition):
        self.current = self.current.get_next()
        self.linearOffset = transitionEvt.offsetFromRoadCenter

    def position(self, positionEvt: LocalizationPosition):
        self.location = positionEvt.locationId

    def to_dict(self):
        data = {
            "name": self.name,
            "lid": self.current.get_layout_id(),
            "linearOffset": self.linearOffset,
            "pieceLocation": self.location,
        }
        return data

    def __str__(self):
        return f"[{self.name}] {self.current}"

    def __repr__(self):
        return self.__str__()
