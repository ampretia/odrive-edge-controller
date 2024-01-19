from anki_support.anki_sdk.track.layout import Layout
from .events import LocalizationPosition, LocalizationTransition
from .car_interface import ICar


class CarPosition:
    def __init__(self, layout: Layout, car: ICar, piece=None):
        self.layout = layout
        self.current = piece
        self.name = car.get_name()

    def set_finish(self):
        self.current = self.layout.get_finish()

    def transistion(self, transitionEvt: LocalizationTransition):
        self.current = self.current.get_next()

    def position(self, positionEvt: LocalizationPosition):
        pass

    def __str__(self):
        return f"[{self.name}] {self.current}"

    def __repr__(self):
        return self.__str__()
