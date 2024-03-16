from .piece import Piece, Type


class Curve(Piece):
    def __init__(self, id: int, turn: str):
        super().__init__(
            id,
            [
                [0, 1],
                [2, 3],
                [4, 5],
                [6, 7],
                [8, 9],
                [10, 11],
                [12, 13],
                [14, 15],
                [16, 17],
                [18, 19],
                [20, 21, 22],
                [23, 24, 25],
                [26, 27, 28],
                [29, 30, 31],
                [32, 33, 34],
                [35, 36, 37],
            ],
            Type.CURVE,
        )

        self.turn = turn

    def to_dict(self):
        return {"lid": self._id, "type": self._type, "turn": self.turn}

    def __str__(self):
        return f"{self._layout_id} / {self._id} | {self._type} | {self.turn}"
