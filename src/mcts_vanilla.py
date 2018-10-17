
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    #Assuming the player goes first
    #node.untried_actions is the list of legal moves
    bestNode = None
    bestValue = -5
    for child in node.child_nodes:
        currentValue = (child.wins/child.visits) + explore_faction*sqrt(log1p(node.visits)/child.visits)
        if currentValue > bestValue:
            bestValue = currentValue
            bestNode = child
    return bestNode
    # Hint: return leaf_node


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    check = None
    for move in node.untried_actions:
        if move not in node.child_nodes
            check = move
    if check != None:
        node.untried_actions.remove(move)
    new_node = MCTSNode(parent = node, parent_action = check, action_list = board.legal_moves(state))
    node.child_nodes[check] = new_node
    return new_node
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    i = 0
    while i < 1000 and board.legal_actions(state) != [] and !(board.is_ended(state)):
        board.next_state(state, random.choice(board.legal_actions))
        i+= 1


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    parent = node
    while(parent != None):
        node.visits += 1
        node.wins += won
        parent = node.parent


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return None
