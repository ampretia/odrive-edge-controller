from .piece import Piece


class Start(Piece):
    ID = 33

    def __init__(self):
        super().__init__(
            Start.ID,
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
            ],
        )
