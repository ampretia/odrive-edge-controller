from .i_piece import IPiece, Connection
from .finish import Finish
from loguru import logger


class Layout:
    def __init__(self, pieces: list[IPiece]):
        self._list = pieces.copy()
        logger.info("Creating layout")
        # iterate over the pieces to create whole track
        try:
            for i, piece in enumerate(self._list):
                next = i + 1 if i < (len(self._list) - 1) else 0
                prev = i - 1 if i > 0 else (len(self._list) - 1)

                piece.set_layout_id(i)
                piece.set_connection(Connection.NEXT, self._list[next])
                piece.set_connection(Connection.PREVIOUS, self._list[prev])

                self._list[i] = piece

            logger.info(self._list)
        except Exception as e:
            logger.error(e)
            raise e

    def get_finish(self):
        for i in range(len(self._list)):
            if type(self._list[i]) is Finish:
                return self._list[i]

    def get_by_index(self, i: int):
        return self._list[i]

    def to_dict(self):
        data = {"name": "layout"}
        data["track"] = [piece.to_dict() for piece in self._list]
        return data

    def __str__(self):
        s = "\n"
        for i, piece in enumerate(self._list):
            # s += f"{i} {piece}"
            next = piece.get_connection(Connection.NEXT)
            prev = piece.get_connection(Connection.PREVIOUS)
            logger.info(f"{next} {prev}")
            nextid = next.get_layout_id() if next is not None else "None"
            previd = prev.get_layout_id() if prev is not None else "None"
            s += f"[{i}] {piece.get_track_id()}  {piece.__class__}  Next> {nextid} Previous> {previd} \n"

        return s

    def __repr__(self):
        return self.__str__()


# #    def __init__(self):
        # self._track_index = _track_index
        # self._position = _position
        # self._offset = _offset
