########################################
# CS63: Artificial Intelligence, Final Project
# Spring 2022, Swarthmore College
########################################
# File taken from lab 4
########################################

from math import log, sqrt
from random import choice

class Node(object):
    """Node used in MCTS"""
    def __init__(self, state):
        self.state = state
        self.children = {} # maps moves to Nodes
        self.visits = 0    # number of times node was in select/expand path
        self.wins = 0      # number of wins for player +1
        self.losses = 0    # number of losses for player +1
        self.value = 0     # value (from player +1's perspective)
        self.untried_moves = list(state.availableMoves) # moves to try

    def updateValue(self, outcome):
        """
        Increments self.visits.
        Updates self.wins or self.losses based on the outcome, and then
        updates self.value.

        This function will be called during the backpropagation phase
        on each node along the path traversed in the selection and
        expansion phases.

        outcome: Who won the game.
                 +1 for a 1st player win
                 -1 for a 2nd player win
                  0 for a draw
        """
        self.visits+=1
        if outcome==1:
            self.wins+=1
        elif outcome==-1:
            self.losses+=1

        self.value=1+((self.wins-self.losses)/self.visits)

        return 0

    def UCBWeight(self, UCB_const, parent_visits, parent_turn):
        """
        Weight from the UCB formula used by parent to select a child.

        This function calculates the weight for JUST THIS NODE. The
        selection phase, implemented by the MCTSPlayer, is responsible
        for looping through the parent Node's children and calling
        UCBWeight on each.

        UCB_const: the C in the UCB formula.
        parent_visits: the N in the UCB formula.
        parent_turn: Which player is making a decision at the parent node.
           If parent_turn is +1, the stored value is already from the
           right perspective. If parent_turn is -1, value needs to be
           converted to -1's perspective.
        returns the UCB weight calculated
        """
        UCB=0
        if parent_turn == 1:
            v=self.value
        else:
            v= 2-self.value
        C=UCB_const
        N=parent_visits
        n=self.visits
        UCB=v+C*sqrt(log(N)/n)

        return UCB

class MCTSPlayer(object):
    """Selects moves using Monte Carlo tree search."""
    def __init__(self, num_rollouts=3000, UCB_const=1.0):
        self.name = "MCTS"
        self.num_rollouts = int(num_rollouts)
        self.UCB_const = UCB_const
        self.nodes = {} # dictionary that maps states to their nodes

    def getMove(self, game_state):
        """
        Finds existing node in tree or create a node for game_state and adds
        it to the tree, calls MCTS to perform rollouts, and returns the best
        move from the current player's perspective
        """
        key=str(game_state)
        if key in self.nodes:
            curr_node=self.nodes[key]
        else:
            curr_node=Node(game_state)
            self.nodes[key]=curr_node
        self.MCTS(curr_node)
        bestValue=-float("inf")
        bestMove=None
        for move, child_node in curr_node.children.items():
            if curr_node.state.turn==1:
                value=child_node.value
            else:
                value=2-child_node.value
            if value>bestValue:
                bestValue=value
                bestMove=move
        return bestMove

    def status(self, node):
        """
        This method is used solely for debugging purposes. Given a
        node in the MCTS tree, reports on the node's data (wins, losses,
        visits, values), as well as the data of all of its immediate
        children. Helps to verify that MCTS is working properly.
        """
        print("node wins ", node.wins,", ", "losses ", node.losses,", ", "visits ",\
         node.visits, "value ", node.value)
        for move, child in node.children.items():
            print("child wins ", child.wins,", ", "losses ", child.losses,", ", \
            "visits ", child.visits, "value ", child.value, ", ", "move", move)


    def selection(self, node):
        """
        Takes in the current node and returns the path of nodes explored based
        on the UCB function.
        """
        path = []
        path.append(node)
        curr_node = node
        while len(curr_node.untried_moves) == 0 and not curr_node.state.isTerminal:
            best_UCB = -1
            best_child = None
            for child in curr_node.children.values():
                child_UCB = child.UCBWeight(self.UCB_const,node.visits,node.state.turn)
                if child_UCB > best_UCB:
                    best_UCB = child_UCB
                    best_child = child
            path.append(best_child)
            curr_node = best_child

        return path

    def expansion(self, node):
        """
        Takes the last node from selection and returns a randomly chosen child
        node. Adds the child node to the children dictionary.
        """
        move = choice(node.untried_moves)
        state = node.state.makeMove(move)
        child_node = Node(state)
        node.untried_moves.remove(move)
        node.children[move]=child_node # update node's children
        key = str(child_node.state)
        if key not in self.nodes: # only add to nodes if not already added
            self.nodes[key] = child_node
        return child_node

    def simulation(self, node):
        """
        Takes a child node, perfoms a roll out, and returns the outcome. Returns
        1 if player 1 wins, -1 if player 2 wins, and 0 if it's a draw.
        """
        current_node = node
        while not current_node.state.isTerminal:
            move = choice(current_node.untried_moves)
            next_state = current_node.state.makeMove(move)
            next_node = Node(next_state)
            current_node = next_node

        return current_node.state.winner

    def backpropagation(self, path, outcome):
        """
        Takes a path and outcome and updates stats for nodes along the path.
        """
        for node in path:
            node.updateValue(outcome)

    def MCTS(self, current_node):
        """
        Plays out random games from the root node to a terminal state.
        Each rollout consists of four phases:
        1. Selection: Nodes are selected based on the max UCB weight.
                      Ends when a node is reached where not all children
                      have been expanded.
        2. Expansion: A new node is created for a random unexpanded child.
        3. Simulation: Uniform random moves are played until end of game.
        4. Backpropagation: Values and visits are updated for each node
                     on the path traversed during selection and expansion.
        Returns: None
        """

        for i in range(self.num_rollouts):
            path = self.selection(current_node)
            selected_node = path[-1]
            if selected_node.state.isTerminal:
                outcome = selected_node.state.winner
            else:
                next_node = self.expansion(selected_node)
                path.append(next_node)
                outcome = self.simulation(next_node)
            self.backpropagation(path, outcome)
