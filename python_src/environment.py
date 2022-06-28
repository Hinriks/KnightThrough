from enum import IntEnum
from inspect import BoundArguments
from operator import length_hint
from os import sep
import random
import itertools
import math
import copy

class State: 
    board = None

    def __init__(self, w, h, r, state=None) -> None:
        self.height = h
        self.width = w
        self.role = r
        if state:
            self.board = copy.deepcopy(state.board)
        else:
            """ self.board =   [["white","white","white","white","white"],
                            ["white","white","white","white","white"],
                            ["","","","",""],
                            ["black","black","black","black","black"],
                            ["black","black","black","black","black"]] """
            self.board = []
            self.board.append(["white"]* w)
            self.board.append(["white"]* w)
            for i in range(h-4):
                self.board.append([""]* w)
            self.board.append(["black"]* w)
            self.board.append(["black"]* w)

    def __str__(self) -> str:
        output = ""
        for line in reversed(self.board):
            for cell in line:
                output += f"{cell:6}"
            output += "\n"
        return output

    def state_evaluation(self):
        # White piece at top
        # Black piece at bottom
        # No moves available = Draw
        # Furthest black piece
        # Furthest white piece
        if "black" in self.board[0]:
            if self.role == "white":
                return -100
            return 100
        if "white" in self.board[self.height-1]:
            if self.role == "white":
                return 100
            return -100
        if not len(self.get_legal_actions(self.role)):
            return 0

        best_white = 0
        best_black = 0
        for y,row in enumerate(self.board):
            for col in row:
                #print (best_white)
                if col == "black" and best_black == 0:
                    best_black = self.height - y
                if col == "white":
                    #print ("White found in row:",y)
                    best_white = y+1 # Offset value since y starts at 0 
        #print (f"best black: {best_black}, best white: {best_white}")
        if self.role == "white":
            return best_white-best_black
        return best_black-best_white

    def check_for_winner(self):
        if "white" in self.board[self.height-1]: return True
        if "black" in self.board[0]: return True
        return False
        
        

    def __hash__(self) -> int:
        pass

    def key(self):
        pass

    def check_outside_boundaries(self, new_loc):
        # Check new X position
        if (new_loc[0] < 0 or new_loc[0] > self.width-1):
            return False
        # Check new Y position
        if (new_loc[1] < 0 or new_loc[1] > self.height-1):
            return False
        return True

    def get_legal_action(self, board, piece_loc, role):
        legal_moves = []

        direction = 1
        if role == "black":
            direction = -1
        
        moves = [[-2,1],[-1,2],[1,2],[2,1]]
        attack_moves = [[-1,1],[1,1]]
        piece_x = piece_loc[0]
        piece_y = piece_loc[1]

        #if board[piece_y][piece_x] != role:
        #    return "ERROR: Not your piece"

        # One up, two left
        for move in moves:
            new_x = piece_x + move[0]*direction
            new_y = piece_y + move[1]*direction
            if self.check_outside_boundaries([new_x, new_y]):
                if board[new_y][new_x] == "":
                    legal_moves.append((piece_x, piece_y, new_x, new_y))
        for move in attack_moves:
            new_x = piece_x + move[0]*direction
            new_y = piece_y + move[1]*direction
            if self.check_outside_boundaries([new_x, new_y]):
                if role == "white":
                    if board[new_y][new_x] == "black":
                        legal_moves.append((piece_x, piece_y, new_x, new_y))
                else:
                    if board[new_y][new_x] == "white":
                        legal_moves.append((piece_x, piece_y, new_x, new_y))

        return legal_moves

    def get_legal_actions(self, role):
        legal_moves = []
        for y,row in enumerate(self.board):
            for x,col in enumerate(row):
                if col == role:
                    moves = self.get_legal_action(self.board, [x,y], role)
                    for move in moves:
                        legal_moves.append(move)
        return legal_moves


class Environment:
    def __init__(self, w, h, r) -> None:
        self.height = h
        self.width = w
        self.role = r
        self.currentState = State(w,h,r)
        print (r)

    def __str__(self) -> str:
        pass

    def do_move(self, move):
        x1 = move[0]-1
        y1 = move[1]-1
        x2 = move[2]-1
        y2 = move[3]-1
        piece = self.currentState.board[y1][x1]
        self.currentState.board[y1][x1] = ""
        self.currentState.board[y2][x2] = piece

        mul = 1
        if self.role == "black":
            mul = -1
        print (self.currentState.state_evaluation()*mul)
            


    def undo_move(state, move):
        pass

    



    def is_terminal(state):
        pass

    def evaluation_function(state):
        pass
    



if '__main__' == __name__:
    env = Environment(5,5)
    print (env.currentState)
    print (env.currentState.get_legal_actions(env.currentState, "white"))
    #print("Initial state")
    #print(env.currentState.board)
    #print("State after white has moved one piece")
    #env.do_move(env.currentState.board, [0,0,1,2])
    #env.do_move(env.currentState.board, [0,4,2,2])
    #print(*env.currentState.board, sep="\n")
    """print(*s.board, sep="\n")
    print("first index is : ", s.board[0])"""
