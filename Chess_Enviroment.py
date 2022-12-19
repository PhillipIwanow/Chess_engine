import chess
import numpy as np
import random as rnd


class Chess_ENV(object):
    
    def __init__(self, opponent_type='random'):
        
        self.oppenent_type = opponent_type
        self.board = chess.Board()
        self.moves = []
        self.turn_tracker = 0
    
    def print_board(self):
        print(self.board)
    
    def print_moves(self):
        print(self.generate_move_list())

    def generate_move_list(self):
        
        self.moves.clear()
        
        moves_t = str(self.board.legal_moves)[37:-1]
        moves_t = moves_t.replace(", ", "', '")
        moves_t = moves_t.replace("(", "('")
        moves_t = moves_t.replace(")", "')")
        moves_t = eval(moves_t)
        
        for i in moves_t:
            self.moves.append(i)
        
        return self.moves
    
    def board_string_to_int(self):
            
        n_board = np.array([])
        switch = {
            'P': 0.1,
            'R': 0.2,
            'N': 0.3,
            'B': 0.4,
            'Q': 0.5,
            'K': 0.6,
            'p': -0.1,
            'r': -0.2,
            'n': -0.3,
            'b': -0.4,
            'q': -0.5,
            'k': -0.6,
            '.': 0,
        }
        for char in str(self.board):
            if char == ' ':
                continue
            elif char != '\n':
                n_board = np.append(n_board, switch.get(char))
        return n_board
    
    def board_state(self):

        if self.board.is_checkmate == True:
            return 1
        
        elif self.board.is_stalemate == True:
            return 0
        
        elif self.board.is_insufficient_material == True:
            return 0
        
        elif self.board.is_seventyfive_moves() == True:
            return 0
        
        elif self.board.is_fivefold_repetition() == True:
            return 0
        
        else:
            return None
    
    def reset(self):
        self.board.reset()
    
    def step(self, action):
        
        if self.turn_tracker == 1:
            self.turn_tracker = 0

        self.board.push_san(action)
        
        if self.board_state() == 1:
            reward = 1000
            if self.turn_tracker == 1:
                reward = -1000
            done = True
        
        elif self.board_state() == 0:
            reward = 50
            done = True
        
        else:
            reward = 0
            done = False

        if self.oppenent_type == 'random':
            move_list = self.generate_move_list()
            self.board.push_san(rnd.choice(move_list))
            if self.board_state() == 1:
                reward = -1000
                done = True
            elif self.board_state() == 0:
                reward = 100
                done = True
            else:
                reward = 0
                done = False

        state = self.board_string_to_int()
        move_list = self.generate_move_list()
        self.turn_tracker = 1

        return state, move_list, reward, done