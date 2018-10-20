Joshua Clouse & Dustin Halsey

For our modified MCTS algorithm we went for a very simple, brute force appraoch. The original heuristic is created by simply making
random moves down the tree and returning the end result. What we did was just ran that simulation 5 times over and took the average
result from that to send it back up the tree. For any heuristic the goal is to have the most detailed information so simply increasing
our sample size accomplished that and gave us dramatically increased results when tested against the vanilla mcts.

Additionally, here is some data to outline our modified MCTS improvements:


MCTS Vanilla vs rollout_bot
Iterations: 100
Vanilla wins: 33
rollout wins:59
ties: 8

MCTS_Modified vs rollout_bot
Iterations: 100
Modified wins: 73
rollout wins: 20
ties: 7

As shown by the winrate increase from 33% to 73%, our modified MCTS has an improvement of intelligence over our vanilla bot.