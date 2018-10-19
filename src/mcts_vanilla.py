
from mcts_node import MCTSNode
from math import sqrt, log
from random import choice

num_nodes = 1000 #the depth of our MCTS.  (num_node iterations of MCTS)
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
    bestValue = -1
    for child in node.child_nodes:
        currentValue = (child.wins/child.visits) + explore_faction*sqrt(log1p(node.visits)/child.visits) #formula for value
        if currentValue > bestValue:
            bestValue = currentValue
            bestNode = child
            print("child bestValue updated")
    if bestNode == None: #if we did not find any children (because we have reached a leaf)
        return node #return the leaf node
    traverse_nodes(bestNode,board,state,identity) #recursively traverse until we reach the best leaf node   
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
        #print(move)
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
        print(board.display(state,move)) #debug to show the progress

    
    winners = board.points_values(state)
    return state #returns the state of the finished board
    #this is gonna be unneccesary
    if winners[1] == 1: #returns 1 if player 1 won
        return 1
    elif winners[1] == -1:
        return 2 #returns 2 if player 2 won
    else:
        return 0 #returns 0 if it was a tie

def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    #once a simulation is complete the result is added to all the nodes that led to that point as well as incrementing the number of visits 
    #for each.
    parent = node
    numOfLoops = 0 #debug
    while(parent.parent_action != None): #changed to parent.parent_action from parent since parent was infinte looping for some reason
        node.visits += 1
        node.wins += won
        parent = node.parent
        print(parent.parent_action)
        numOfLoops += 1 #debug
    print("Num of loops in back propagate: ",numOfLoops) #debug
    print("Num of node visits in back propagate: ",node.visits) #debug
    return

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
    #for step in range(num_nodes):
    for i in range(1,2): #temp range for debugging. trying to get 1 successful iteration first   
        # Copy the game for sampling a playthrough (before extending the tree)
        sampled_game = state

        # Start at root
        node = root_node
        node = traverse_nodes(node, board, sampled_game, identity_of_bot) #updates node to be the leaf node with the best perceived chance of winning (the node to expand)

        new_node = expand_leaf(node,board,sampled_game) #adds a random new leaf from possible moves
        sampled_game = board.next_state(sampled_game, new_node.parent_action) #updates the copied state to include the move explored by expand_leaf
        #print(board.display(sampled_game,new_node.parent_action)) #prints the action created by expand_leaf

        #We then simulate the node
        state_finished = rollout(board, sampled_game)
        #get the value for the win and push it back up the tree
        wonDict = board.points_values(state_finished)
        backpropagate(new_node, wonDict[identity_of_bot])
        print("Num of node visits at root:" ,node.visits) #debug. this should be 1 right now, but is comng up as 0

    #should look at all the children nodes and see which one yeilds the best score.
    """
    for n in root_node.child_nodes:
        score = n.wins/n.visits
        if(score > best):
            bestMove = n.parent_action
            bestScore = score
    """
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    print("leaving mcts_vanilla.think()") #debug
    return bestMove
