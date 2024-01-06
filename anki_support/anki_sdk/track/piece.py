from .i_piece import IPiece, Connection

from typing import List


class Piece(IPiece):
    def __init__(self, id: int, locations: List[List[int]]):
        self._id = id
        self._locations = locations
        self._reversed = False
        self._next: IPiece = None
        self._previous: IPiece = None
        self._connections: dict[Connection, IPiece] = {}
        self._layout_id = -1

    def get_track_id(self):
        return self._id

    def __str__(self):
        return f"{self.__class__} {self._id} {self._locations}"

    def __repr__(self) -> str:
        return self.__str__()

    # def reverse(self):
    #     self._locations.reverse()
    #     self._locations.forEach(line => line.reverse())
    #     self._reversed = !self._reversed

    #     get locations(): number[][]
    # return self._locations

    def set_connection(self, dir: Connection, piece: IPiece):
        self._connections[dir] = piece

    def get_connection(self, dir: Connection) -> IPiece | None:
        return self._connections[dir]

    def set_layout_id(self, layout_id: int):
        self._layout_id = layout_id

    def get_layout_id(self) -> int:
        return self._layout_id

    #     public distance(locationId1: number, locationId2: number): number
    # return Math.abs(
    #     self.getIndexByLocationId(locationId1)
    #     - self.getIndexByLocationId(locationId2)
    # )

    def is_reversed(self) -> bool:
        return self._reversed
