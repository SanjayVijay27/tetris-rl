import numpy as np
import random
import math
import time
import cv2
import copy
import pydirectinput

from tetris_game_state import TetrisGameState

input_dict = {"move_left":"left", "move_right":"right", "rotate":"d", "drop":"s"}

class Node:
    def __init__(self, game_state, parent=None):
        self.game_state = game_state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.total_score = 0
    
    def expand(self, action):
        child_game_state = self.game_state.apply_action(action) # get game state after performing action
        child_node = Node(child_game_state, self)   # create child node with that game state
        self.children.append(child_node)
        return child_node
    
    def is_fully_expanded(self):
        return len(self.children) == len(self.game_state.get_possible_actions())
    
    def rollout(self):
        return self.game_state.rollout()
    
    def back_propagate(self, reward):
        self.visits += 1
        self.total_score += reward
        if self.parent is not None:
            self.parent.back_propagate(reward)

    def is_terminal(self):
        return self.game_state.is_terminal()    # a terminal node is a node whose game state is terminal, not necessarily a node with no children
    
    def find_best_child(self, exploration_constant=1.0):
        def uct_score(node):
            exploitation = node.total_score / node.visits
            exploration = math.sqrt(2 * math.log(self.visits) / node.visits)
            return exploitation + exploration_constant * exploration
        if len(self.children) == 0:
            return self
        return max(self.children, key=uct_score)

def mcts(node, num_simulations, exploration_constant=1.0):
    for i in range(num_simulations):
        current_node = node
        while not current_node.is_terminal() and current_node.is_fully_expanded():
            current_node = current_node.find_best_child(exploration_constant)
            print("selected best child")

            # board = current_node.game_state.board * 255
            # board = board.astype(np.uint8)
            # resized = cv2.resize(board, (600, 600), interpolation = cv2.INTER_AREA)

            # cv2.imshow('Image', resized)
            # cv2.waitKey(1)
        #print(current_node.is_terminal())
        if not current_node.is_terminal():
            untried_actions = set(current_node.game_state.get_possible_actions()) - set([child.game_state.get_last_action() for child in current_node.children])
            print(list(untried_actions))
            print("possible " + str(set(current_node.game_state.get_possible_actions())))
            print("tried " + str(set([child.game_state.get_last_action() for child in current_node.children])))
            #print(untried_actions)
            if (len(untried_actions) <= 0):
                print("untried is empty")
            else:
                action = random.choice(list(untried_actions))
                print("action " + str(action))
                current_node = current_node.expand(action)  # creates child node for current node and sets current node to child node created by expansion

            # board = current_node.game_state.board * 255
            # board = board.astype(np.uint8)
            # resized = cv2.resize(board, (600, 600), interpolation = cv2.INTER_AREA)

            # cv2.imshow('Image', resized)
            # cv2.waitKey(1)
        reward = current_node.rollout()
        #print(reward)
        current_node.back_propagate(reward)
    # cv2.destroyAllWindows()
    # board = current_node.game_state.board * 255
    # board = board.astype(np.uint8)
    # resized = cv2.resize(board, (600, 600), interpolation = cv2.INTER_AREA)

    # cv2.imshow('Image', resized)
    # cv2.waitKey(0)
    print("mcts called")
    return node.find_best_child(0)

if __name__ == "__main__":
    time.sleep(3)
    game_state = TetrisGameState.initial_state()    # initial state of the Tetris game
    root_node = Node(copy.deepcopy(game_state))
    moves = []
    while not game_state.is_terminal():
        # print(game_state.board)
        best_child = mcts(root_node, num_simulations=1000)
        best_action = best_child.game_state.get_last_action()
        moves.append(best_action)
        game_state = game_state.apply_action(best_action)
        pydirectinput.press(input_dict[best_action])
        root_node = best_child
        # print(game_state.board)

        board = game_state.board * 255
        board = board.astype(np.uint8)
        resized = cv2.resize(board, (600, 600), interpolation = cv2.INTER_AREA)

        cv2.imshow('Image', resized)
        cv2.waitKey(1)
        
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break
        #time.sleep(0.1)
    cv2.destroyAllWindows()
    print(moves)

# documentation