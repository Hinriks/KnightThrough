from copy import deepcopy
import random
import time
import math

from environment import Environment
#############

MAX_DEPTH = 18

"""Agent acting in some environment"""


class Agent(object):

    # this method is called on the start of the new environment
    # override it to initialise the agent
    def start(self, role, width, height, play_clock):
        print("start called")
        return

    # this method is called on each time step of the environment
    # it needs to return the action the agent wants to execute as a string
    def next_action(self, last_move):
        print("next_action called")
        return "NOOP"

    # this method is called when the environment has reached a terminal state
    # override it to reset the agent
    def cleanup(self, last_move):
        print("cleanup called")
        return


#############

class MyAgent(Agent):
    role = None
    play_clock = None
    my_turn = False
    width = 0
    height = 0

    # start() is called once before you have to select the first action. Use it to initialize the agent.
    # role is either "white" or "black" and play_clock is the number of seconds after which nextAction must return.
    def start(self, role, width, height, play_clock):
        self.play_clock = play_clock
        self.role = role
        self.my_turn = role != 'white'
        # we will flip my_turn on every call to next_action, so we need to start with False in case
        #  our action is the first
        self.width = width
        self.height = height
        self.abort_search = False
        # TODO: add your own initialization code here
        self.env = Environment(width, height, role)
        self.alphacounter = 0
        self.betacouter = 0
        return

    def minimax(self, pos, depth, max_role, alpha, beta, state):
        if depth == 0 or state.check_for_winner():
            return state.state_evaluation()
            
        #print (time.process_time() - self.start_time)
        if time.process_time() - self.start_time > self.play_clock-1:
            raise TimeoutError

        if self.role == "white":
            min_role = "black"
        else:
            min_role = "white"

        
        if max_role:
            maxEval = -math.inf
            for move in self.env.currentState.get_legal_action(self.env.currentState.board, pos, self.role):
                #print ("move:", move)
                new_state = deepcopy(state)
                # Do each move in a new copy
                x1 = move[0]
                y1 = move[1]
                x2 = move[2]
                y2 = move[3]
                new_state.board[y1][x1] = ""
                new_state.board[y2][x2] = self.role
                self.states_expanded += 1
                eval = self.minimax([move[2],move[3]], depth-1, False, alpha, beta, new_state)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    self.alphacounter += 1
                    break
            return maxEval

        else:
            minEval = math.inf
            for move in self.env.currentState.get_legal_action(self.env.currentState.board, pos, min_role):
                new_state = deepcopy(state)
                # Do each move in a new copy
                x1 = move[0]
                y1 = move[1]
                x2 = move[2]
                y2 = move[3]
                new_state.board[y1][x1] = ""
                new_state.board[y2][x2] = min_role
                self.states_expanded += 1
                eval = self.minimax([move[2],move[3]], depth-1, True, alpha, beta, new_state)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    self.betacouter += 1
                    break
            return minEval

    def stop_search(self):
        self.abort_search = True


    def next_action(self, last_action):
        if last_action:
            if self.my_turn and self.role == 'white' or not self.my_turn and self.role != 'white':
                last_player = 'white'
            else:
                last_player = 'black'
            
            print("%s moved from %s to %s" % (last_player, str(last_action[0:2]), str(last_action[2:4])))
            # TODO: 1. update your internal world model according to the action that was just executed
            self.env.do_move(last_action)
        else:
            print("first move!")

        # update turn (above that line it myTurn is still for the previous state)
        self.my_turn = not self.my_turn
        legal_moves = []
        self.abort_search = False

        if self.my_turn:
            self.states_expanded = 0
            try:
                # Iterative deepening
                self.start_time = time.process_time()
                for d in range(MAX_DEPTH):
                    print (f"---- DEPTH {d} ----")
                    print (f"States expanded: {self.states_expanded}")
                    print (f"Time passed: {time.process_time()-self.start_time}")
                    if self.abort_search:
                        break
                    legal_moves = self.env.currentState.get_legal_actions(self.role)
                    move_values = [0] * len(legal_moves)
                    for i,move in enumerate(legal_moves):
                        # Make a copy of the current state
                        state = deepcopy(self.env.currentState)
                        # Do each move in a new copy
                        x1 = move[0]
                        y1 = move[1]
                        x2 = move[2]
                        y2 = move[3]
                        state.board[y1][x1] = ""
                        state.board[y2][x2] = self.role
                        self.states_expanded += 1
                        # Get minimax eval for each move
                        move_values[i] = self.minimax([move[2], move[3]], d, True, -math.inf, math.inf, state)
                    if 100 in move_values:
                        print ("Winning state found at depth:", d)
                        self.stop_search()
                    
                    #print ("legal moves:", legal_moves)
                    #print ("move values:", move_values)

                
                    
            except TimeoutError:
                print ("Time over")
            print ("Alpha:",self.alphacounter, ", Beta:", self.betacouter)
            best_move_value = max(move_values)
            best_move_index = move_values.index(best_move_value)
            best_move = legal_moves[best_move_index] 

            print (f"Best legal move is", best_move, "with eval", best_move_value)
            print (f"Total Time: {time.process_time() - self.start_time}")
            print (f"Total states expanded: {self.states_expanded}")
            
            print ("AGENT MAKING MOVE", best_move[0]+1, best_move[1]+1, best_move[2]+1, best_move[3]+1)
            return f"(move {best_move[0]+1} {best_move[1]+1} {best_move[2]+1} {best_move[3]+1})"
        else:
            return "noop"



"""A random Agent for the KnightThrough game

 RandomAgent sends actions uniformly at random. In particular, it does not check
 whether an action is actually useful or legal in the current state.
 """


class RandomAgente(Agent):
    role = None
    play_clock = None
    my_turn = False
    width = 0
    height = 0

    # start() is called once before you have to select the first action. Use it to initialize the agent.
    # role is either "white" or "black" and play_clock is the number of seconds after which nextAction must return.
    def start(self, role, width, height, play_clock):
        self.play_clock = play_clock
        self.role = role
        self.my_turn = role != 'white'
        # we will flip my_turn on every call to next_action, so we need to start with False in case
        #  our action is the first
        self.width = width
        self.height = height
        # TODO: add your own initialization code here
        return

    def next_action(self, last_action):
        if last_action:
            if self.my_turn and self.role == 'white' or not self.my_turn and self.role != 'white':
                last_player = 'white'
            else:
                last_player = 'black'
            print("%s moved from %s to %s" % (last_player, str(last_action[0:2]), str(last_action[2:4])))
            # TODO: 1. update your internal world model according to the action that was just executed
        else:
            print("first move!")

        # update turn (above that line it myTurn is still for the previous state)
        self.my_turn = not self.my_turn
        if self.my_turn:
            # TODO: 2. run alpha-beta search to determine the best move

            # Here we just construct a random move (that will most likely not even be possible),
            # this needs to be replaced with the actual best move.
            x1 = random.randint(1, self.width)
            x2 = x1 + random.randint(1, 2) * random.choice([-1, 1])
            y1 = random.randint(1, self.height)
            direction = 1
            if self.role == 'black':
                direction = -1
            y2 = y1 + direction * random.randint(1, 2)
            return "(move " + " ".join(map(str, [x1, y1, x2, y2])) + ")"
        else:
            return "noop"


