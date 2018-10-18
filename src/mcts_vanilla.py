
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
    #simply uses the formula and finds which node should be expanded on
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
    #Once we have a node that needs to be expanded, this function looks at all the valid moves, checks to see if the valid move is
    #yet in the child dict. If it's not it gets added into the child dict and then gets returned. This method should be called multiple times
    #in think, one for each new node
    check = None
    for move in node.untried_actions:
        if move not in node.child_nodes.keys()
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
    #basically while there are valid moves, the amount of iterations are less than 1000, and the games hasn't ended, the loop
    #will keep looking for a random legal move and play it
    i = 0
    while i < num_nodes and board.legal_actions(state) != [] and !(board.is_ended(state)):
        board.next_state(state, random.choice(board.legal_actions))
        i+= 1


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    #once a simulation is complete the result is added to all the nodes that led to that point as well as incrementing the number of visits 
    #for each.
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
    #this is where the real shit happens and we need to call all those funcitons, should be relatively simple, just need to make a loop
    #which goes to either when the game ends, or there are no more valid moves. With each iteration of the loop we must apply the functions
    #in order. Remember that rollout must be called multiple times for each child node of the node that is to be expanded upon i.e. on the
    #node that was chosen by expand_leaf().
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        #This should select the node we want to expand
        node = traverse_nodes(node, sampled_game, identity_of_bot)
        #this expands that leaf node into some child nodes to simulate
        node = expand_leaf(node, board, sampled_game)
        #We then simulate the node
        rollout(board, sampled_game)
        #get the value for the win and push it back up the tree
        backpropagate(node, win_values(board, sampled_game)[identity_of_bot])

        #This should loop through all the nodes in order to find the path with the highets outcome
        bestScore = -5
        bestMove = None
        #should look at all the children nodes and see which one yeilds the best score.
        for(n in root_node.child_nodes):
            score = n.wins/n.visits
            if(score > best):
                bestMove = n.parent_action
                bestScore = score
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return bestMove
