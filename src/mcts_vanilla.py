
from mcts_node import MCTSNode
from copy import deepcopy
from math import sqrt, log, log1p
from random import choice

num_nodes = 1000 #the depth of our MCTS.  (num_node iterations of MCTS)
explore_faction = 2.

#for some reason we are getting a nonType return as soon as we branch larger than the starting node's size
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
    #if not node.child_nodes:
    #   node.visits +=1
    #    return node
    bestNode = None
<<<<<<< HEAD
    bestValue = None
    for child in node.child_nodes:
        child = node.child_nodes[child]
        #print("Child Wins: ", child.wins) #wins
        currentValue = (child.wins/child.visits) + explore_faction*(sqrt(log1p(node.visits)/child.visits)) #formula for value
        if bestValue == None or currentValue > bestValue:
            bestValue = currentValue
            bestNode = child
            #print("child bestValue updated")
        state = board.next_state(state, child.parent_action)
    if bestNode == None or len(node.untried_actions)>0: #if we did not find any children or we have reached a node with an untried action(because we have reached a leaf)
        #print("Node wins in: ", node.wins)
        return node #return the leaf node that we will expand upon
    return traverse_nodes(bestNode,board,state,identity) #recursively traverse until we reach the best leaf node

=======
    bestValue = -1000
    stateMove = None

    while(len(node.untried_actions)<=0):    
        for child in node.child_nodes:
            childValue = node.child_nodes[child] #the child node
            currentValue = (childValue.wins/childValue.visits) + explore_faction*sqrt(log1p(node.visits)/childValue.visits) #formula for value
            if currentValue > bestValue: #if we have found a better node
                bestValue = currentValue
                bestNode = childValue
                stateMove = child
        if not bestNode == None: #if we founda  best node, update node
            node = bestNode
            bestNode = None
            bestValue = -1000
            stateMove = None
    return node #return the leaf node that we will expand upon   
>>>>>>> f4948de6d9ae95308b849dd2f499595207d1bc2d
    # Hint: return leaf_node



#expands 1 leaf at a time from node
#returns the new leaf
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
    new_node = None
    if node.untried_actions != []:
        move = choice(node.untried_actions) #get a random unexplored node
        new_node = MCTSNode(parent = node, parent_action = move, action_list = board.legal_actions(board.next_state(state,move)))
        #moves the untried action to the child node since we have now tried it
        node.child_nodes[move] = new_node
        node.untried_actions.remove(move)
        return new_node
    else:
        raise Exception("\n\nFAILURE IN expand_leaf().  node.untried_actions was empty!\n\n") #bad if we get here
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    #basically while there are valid moves, the amount of iterations are less than 1000, and the games hasn't ended, the loop
    #will keep looking for a random legal move and play it
    
    while not board.is_ended(state): #while the game isnt over
        move = choice(board.legal_actions(state)) #choose a random move from legal actions
        state = board.next_state(state, move)
    return state #returns the state of the finished board

def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while(node.parent != None):
        node.visits += 1
        if(won == 1):
            node.wins += 1
        node = node.parent
    node.visits += 1
    if(won == 1):
        node.wins += 1
    
def getCurrentState(node, state, board):
    actions=[]
    while(node.parent_action != None):
        actions.insert(0, node.parent_action)
        node = node.parent
    for action in actions:
        state = board.next_state(state, action)

def getCurrentState(node,board,state):
    statePath = []
    while node.parent_action is not None:
        statePath.insert(0,node.parent_action)
        node = node.parent
    for path in statePath:
        state = board.next_state(state, path)
    return state

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
    identity_of_bot = board.current_player(state) #holds what player this bot is
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    #This should loop through all the nodes in order to find the path with the highets outcome
    bestScore = -5
    bestMove = None
    for step in range(num_nodes):
    #for i in range(1,1000): #temp range for debugging. trying to get 1 successful iteration first   
        # Copy the game for sampling a playthrough (before extending the tree)
        sampled_game = state + tuple()
        node = root_node

        #print("traverse_nodes()")
        node = traverse_nodes(node, board, sampled_game, identity_of_bot) #updates node to be the leaf node with the best perceived chance of winning (the node to expand)
<<<<<<< HEAD
        #sampled_game = getCurrentState(node, sampled_game, board)#print("Node wins:", node.wins)
=======
        sampled_game = getCurrentState(node, board, state + tuple())

        #print("expand_leaf()")
>>>>>>> f4948de6d9ae95308b849dd2f499595207d1bc2d
        new_node = expand_leaf(node,board,sampled_game) #adds a random new leaf from possible moves
        sampled_game = getCurrentState(new_node, board, state + tuple())
        #print(board.display(sampled_game,new_node.parent_action)) #prints the action created by expand_leaf
        #print("rollout()")
        state_finished = rollout(board, sampled_game)
        #print("backpropagate()")
        backpropagate(new_node, board.points_values(state_finished)[identity_of_bot])
        #should look at all the children nodes and see which one yeilds the best score.
        #print("End")
    for n in root_node.child_nodes:
        child = root_node.child_nodes[n]
        score = child.wins/child.visits
        if(score > bestScore):
            bestMove = child.parent_action
            bestScore = score
    
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
<<<<<<< HEAD
    #print("leaving mcts_vanilla.think()") #debug
=======
    # print("leaving mcts_vanilla.think()") #debug
>>>>>>> f4948de6d9ae95308b849dd2f499595207d1bc2d
    return bestMove
