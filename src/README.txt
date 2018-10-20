Joshua Clouse & Dustin Halsey

For our modified MCTS algorithm we went for a very simple, brute force appraoch. The original heuristic is created by simply making
random moves down the tree and returning the end result. What we did was just ran that simulation 5 times over and took the average
result from that to send it back up the tree. For any heuristic the goal is to have the most detailed information so simply increasing
our sample size accomplished that and gave us dramatically increased results when tested against the vanilla mcts.