import numpy as np

class board_state():
    
    TETROMINOES = {
        'I': [
            np.array([
                [True, True, True, True]
            ], dtype=bool),
            np.array([
                [True],
                [True],
                [True],
                [True]
            ], dtype=bool)
        ],
        'O': [
            np.array([
                [True, True],
                [True, True]
            ], dtype=bool)
        ],
        'T': [
            np.array([
                [False, True, False],
                [True, True, True]
            ], dtype=bool),
            np.array([
                [True, False],
                [True, True],
                [True, False]
            ], dtype=bool),
            np.array([
                [True, True, True],
                [False, True, False]
            ], dtype=bool),
            np.array([
                [False, True],
                [True, True],
                [False, True]
            ], dtype=bool)
        ],
        'L': [
            np.array([
                [True, False],
                [True, False],
                [True, True]
            ], dtype=bool),
            np.array([
                [True, True, True],
                [True, False, False]
            ], dtype=bool),
            np.array([
                [True, True],
                [False, True],
                [False, True]
            ], dtype=bool),
            np.array([
                [False, False, True],
                [True, True, True]
            ], dtype=bool)
        ],
        'J': [
            np.array([
                [False, True],
                [False, True],
                [True, True]
            ], dtype=bool),
            np.array([
                [True, False, False],
                [True, True, True]
            ], dtype=bool),
            np.array([
                [True, True],
                [True, False],
                [True, False]
            ], dtype=bool),
            np.array([
                [True, True, True],
                [False, False, True]
            ], dtype=bool)
        ],
        'S': [
            np.array([
                [False, True, True],
                [True, True, False]
            ], dtype=bool),
            np.array([
                [True, False],
                [True, True],
                [False, True]
            ], dtype=bool)
        ],
        'Z': [
            np.array([
                [True, True, False],
                [False, True, True]
            ], dtype=bool),
            np.array([
                [False, True],
                [True, True],
                [True, False]
            ], dtype=bool)
        ],
    }

    def __init__(self):
        self.width = 10
        self.height = 20
        self.board = np.full((self.height, self.width), False, dtype=bool)
