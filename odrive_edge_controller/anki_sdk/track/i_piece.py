# /**
#  * Abstract description of a single road piece. Each road piece has a not unique [[id]] and a matrix of [[locations]].
#  * Road pieces can have different characteristics like curve or straight. The [[locations]] matrix varies depending on
#  * the characteristic.
#  *
#  * @since 1.0.0
#  */
from enum import Enum, auto

from abc import ABC, abstractmethod
from typing import Self, Any


class Connection(Enum):
    PREVIOUS = auto()
    NEXT = auto()
    NORTH = auto()
    SOUTH = auto()
    WEST = auto()
    EAST = auto()


class IPiece(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_track_id(self):
        pass

    @abstractmethod
    def set_connection(self, dir: Connection, piece: Self):
        pass

    @abstractmethod
    def get_connection(self, dir: Connection) -> Self | None:
        pass

    @abstractmethod
    def set_layout_id(self, layout_id: int):
        pass

    @abstractmethod
    def get_layout_id(self) -> int:
        pass

#     /**
#      * Matrix of locations. Each location is a specific position on the piece that triggers an event when a vehicle
#      * detects it with its sensor.
#      */
#     locations: number[][]

#     /**
#      * Identifier if the piece. Different pieces may have the same identifier.
#      */
#     id: number

#     /**
#      * The next [[IPiece]] connected to this piece.
#      */
#     next: IPiece

#     /**
#      * The previous [[IPiece]] connected to this piece.
#      */
#     previous: IPiece

#     /**
#      * Indicates if a piece is reversed or not.
#      */
#     reversed: boolean

#     distance(locationId1: number, locationId2: number): number

#     getFirstLocationId(index: number): number

#     getLastLocationId(index: number): number

#     getIndexByLocationId(locationId: number): number

#     /**
#      * Reverses the locations matrix, needed if a piece is connected with a different orientation. Changes the [[reversed]]
#      * state after execution.
#      */
#     reverse(): void

# }

# export {IPiece}
