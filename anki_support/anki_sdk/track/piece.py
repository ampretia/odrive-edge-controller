from .i_piece import IPiece

from typing import List

class Piece(IPiece):
    _id: int
    _next: IPiece
    _previous: IPiece
    _locations: List[List[int]]
    _reversed: bool

    def __init__(self, id: int, locations: List[List[int]]):
    
        self._id = id
        self._locations = locations
        self._reversed = False
    
    def get_track_id(self):
        return self._id
    
    def __str__(self):
        return f"{self.__class__} {self._id} {self._locations}"
    
    def __repr__(self) -> str:
        return self.__str__()

#     public reverse(): void
#     self._locations.reverse()
# self._locations.forEach(line => line.reverse())
# self._reversed = !self._reversed
    

#     get locations(): number[][]
# return self._locations
    

#     get id(): number
# return self._id
    

#     get next(): IPiece
# return self._next
    

#     set next(piece: IPiece)
# self._next = piece
    

#     get previous(): IPiece
# return self._previous
    

#     set previous(piece: IPiece)
# self._previous = piece
    

#     public distance(locationId1: number, locationId2: number): number
# return Math.abs(
#     self.getIndexByLocationId(locationId1)
#     - self.getIndexByLocationId(locationId2)
# )
    

#     public getFirstLocationId(index: number): number
# if (!self._locations[index])
#     throw new Error(`Index [$index] is out of bound.`)

# return self._locations[index][0]
    

#     public getLastLocationId(index: number): number
# return self._locations[index][self._locations[index].length - 1]
    

#     get reversed(): boolean
# return self._reversed
    

#     public getIndexByLocationId(locationId: number): number
# for (let i = 0 i <self._locations.length i++)
#     const index = self.locations[i].indexOf(locationId)
# if (index >= 0) return index  1

# throw new Error(`Location with id [$locationId] does not exist.`)
