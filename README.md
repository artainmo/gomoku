# gomoku

42 school [subject](https://cdn.intra.42.fr/pdf/pdf/81333/en.subject.pdf).

Gomoku game website. Using min-max AI algorithm to simulate a dominant gomoku player.

I will use python as it is more convenient for algorithm/AI projects.<br>
As web framework I will use python flask over python django as python flask is sufficient for what I need and is faster to setup.

## Use
Run flask app on 127.0.0.1:5000: `flask --app Gomoku run`.

Launch with hot-reload: `flask --app Gomoku --debug run`.

If access to 127.0.0.1 gets denied:
* Go to 'chrome://net-internals/#sockets' and flush socket pools.
* [Clear cache and cookies.](https://support.google.com/accounts/answer/32050?hl=en&co=GENIE.Platform%3DDesktop)
* If necessary use a different port using associated flag `flask run --port 8000`.

## Preliminary Notions
### Gomoku and Go
Gomoku is also called five-in-a-row. It is played on a Go board by two players.<br>
Go is an abstract strategy game in which the aim is to surround more territory than the opponent. The game was invented in China 4,500 years ago and is believed to be the oldest board game continuously played to the present day. The conventional board has a size of 19x19, the number of legal board positions in Go has been calculated to be approximately 2.1x10^107.<br>
Gomoku is played with same equipment as Go, however Gomoku is simpler due to five pawns in a row being sufficient for a win.

Different versions and rules around the Gomoku game exist. To generalize, the main goal of this game is to be the first player to place five pawns in a row on the board horizontally, vertically or diagonally. Players take turns placing a pawn on the empty intersection of their choice. Black pawns start.

### Minimax algorithm
The minimax algorithm helps find the best move, by working backwards from the end of the game. At each step it assumes that player A is trying to maximize the chances of A winning, while on the next turn player B is trying to minimize the chances of A winning (i.e., to maximize B's own chances of winning).

Alpha-beta pruning is a technique used in a minimax algorithm to make it faster
by preventing computations that are not necessary as they would not affect the outcome.

## Resources
[codecademy - Learn Flask](https://www.codecademy.com/learn/learn-flask)<br>
[wikipedia - Go](https://en.wikipedia.org/wiki/Go_%28game%29)<br>
[youtube - How to play Gomoku (5 in a row)](https://www.youtube.com/watch?v=-KD743yNDHc)<br>
[wikipedia - Minimax](https://en.wikipedia.org/wiki/Minimax)<br>
[youtube - What is the Minimax Algorithm? - Artificial Intelligence](https://www.youtube.com/watch?v=KU9Ch59-4vw)<br>
[youtube - Algorithms Explained – minimax and alpha-beta pruning](https://www.youtube.com/watch?v=l-hh51ncgDI)<br>
[Iowa State University thesis - New Heuristic Algorithm to improve the Minimax for Gomoku Artificial Intelligence](https://dr.lib.iastate.edu/server/api/core/bitstreams/39a805d5-8f5b-41e6-b07c-19c07229f813/content)<br>
[UCT-ADP Progressive Bias Algorithm for Solving Gomoku](https://arxiv.org/pdf/1912.05407.pdf)<br>
