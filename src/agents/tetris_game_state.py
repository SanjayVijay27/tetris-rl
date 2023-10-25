import numpy as np
import random
import time

class TetrisGameState:

    def __init__(self, board, current_piece, upcoming_pieces): # added last_action attribute for get_last_action
        self.board = board
        self.current_piece = current_piece
        self.upcoming_pieces = upcoming_pieces
        self.piece_position = (0, (self.board.shape[1] - self.current_piece.shape[1]) // 2)
        self.last_action = None
    
    def init_board(self, width=10, height=20):
        board = np.full((height, width), False, dtype=bool)
        return board

    def move_piece(self, row_offset, column_offset):
        new_y = self.piece_position[0] + row_offset
        new_x = self.piece_position[1] + column_offset
        if self.is_valid_position(new_y, new_x, self.current_piece):
            self.piece_position = (new_y, new_x)
            return True
        return False

    def rotate_piece(self): # ISSUE: add direction of rotation
        new_rotation = np.rot90(self.current_piece)
        if self.is_valid_position(self.piece_position[0], self.piece_position[1], new_rotation):
            self.current_piece = new_rotation
            return True
        return False
    
    def is_valid_position(self, row, column, piece):
        # checks if piece would exist outside of the field
        # print(row, column)
        # print(piece)
        # print(self.board)
        piece_height, piece_width = piece.shape
        for r in range(piece_height):
            for c in range(piece_width):
                if piece[r, c]:
                    board_row = r + row
                    board_column = c + column
                    if board_row < 0 or board_row >= self.board.shape[0] or board_column < 0 or board_column >= self.board.shape[1]:
                        #print("false")
                        return False
                    if self.board[board_row, board_column]:
                        #print("false")
                        return False         
        #print("true!!!!!!!!!!!!!!!!!!!!!!!!!")
        #time.sleep(0.5)
        return True

    def place_and_clear_lines(self):
        piece_height, piece_width = self.current_piece.shape
        for r in range(piece_height):
            for c in range(piece_width):
                if self.current_piece[r, c]:
                    self.board[self.piece_position[0]+r, self.piece_position[1]+c] = True
        # checks for full rows and clears lines

        # lines_cleared = 0
        # for row in range(self.board.shape[1]-1, -1, -1):    # iterates backwards to avoid skipping rows after deletions
        #     if sum(self.board[row]) == self.board.shape[1]:
        #         lines_cleared += 1
        #         np.delete(self.board, row, axis=0)  # clears lines of full row by deleting the row
        #         self.board = np.vstack([[False]*self.board.shape[1], self.board])   # replaces deleted row with a new empty row at the top of the field
        # return lines_cleared

        lines_cleared = 0
        score = 0
        new_board = []
        for row in self.board:
            if not np.all(row):
                new_board.append(row)
            else:
                lines_cleared += 1
                score += 1
        while lines_cleared > 0:
            new_board.insert(0, np.full(self.board.shape[1], False, dtype=bool))
            lines_cleared -= 1
        self.board = np.array(new_board, dtype=bool)
        return score
    
    def step(self):
        if not self.move_piece(1, 0):
            self.place_and_clear_lines()
            # updates current piece and upcoming pieces
            self.current_piece = self.upcoming_pieces.pop(0)
            self.upcoming_pieces.append(self.random_piece())
            self.piece_position = (0, (self.board.shape[1] - self.current_piece.shape[1]) // 2)
            if not self.is_valid_position(self.piece_position[0], self.piece_position[1], self.current_piece):
                return False
        return True
    
    def get_possible_actions(self):
        #"move_left", "move_right", "rotate", 
        actions = ["move_left", "move_right", "rotate", "drop"]
        # if self.is_valid_position(self.piece_position[0], self.piece_position[1]-1, self.current_piece):
        #     actions.append("move_left")
        # if self.is_valid_position(self.piece_position[0], self.piece_position[1]+1, self.current_piece):
        #     actions.append("move_right")
        # if self.is_valid_position(self.piece_position[0], self.piece_position[1], np.rot90(self.current_piece)):
        #     actions.append("rotate")
        print(actions)
        return actions
    
    def get_last_action(self):
        return self.last_action

    def apply_action(self, action):
        game_state = TetrisGameState(self.board.copy(), self.current_piece.copy(), self.upcoming_pieces.copy())   #last_action
        game_state.piece_position = self.piece_position
        if action == "move_left":
            game_state.move_piece(0, -1)
        elif action == "move_right":
            game_state.move_piece(0, 1)
        elif action == "rotate":
            game_state.rotate_piece()
        elif action == "drop":
            while game_state.move_piece(1, 0):
                pass
        game_state.step()
        #print(action)
        game_state.last_action = action #last_action
        return game_state

    def is_terminal(self):
        return not self.step()
    
    def rollout(self):
        game_state = self
        lines_cleared = 0
        while not game_state.is_terminal():
            action = random.choice(game_state.get_possible_actions())
            game_state = game_state.apply_action(action)
            lines_cleared += game_state.place_and_clear_lines()   #replaced self with game_state
        return lines_cleared

    @staticmethod
    def random_piece():

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

        return random.choice(list(TETROMINOES.values()))[0]
    
    # @classmethod
    # def initial_state(cls, width=10, height=20, num_upcoming_pieces=4, current_piece=None, upcoming_pieces=None):
    #     if current_piece is None:
    #         current_piece = cls.random_piece()
    #     if upcoming_pieces is None:
    #         upcoming_pieces = [cls.random_piece() for i in range(num_upcoming_pieces)]
    #     board = cls.init_board(width, height)
    #     return cls(board, current_piece, upcoming_pieces)
    
    @classmethod
    def initial_state(cls, width=10, height=20, num_upcoming_pieces=4):
        
        def create_board(width, height):
            return np.full((height, width), False, dtype=bool)

        board = create_board(width, height)
        current_piece = cls.random_piece()
        upcoming_pieces = [cls.random_piece() for _ in range(num_upcoming_pieces)]
        return cls(board, current_piece, upcoming_pieces)