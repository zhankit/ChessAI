## Project for CO456 Game theory
Contributer: Ding Zhan Chia, Meiou Wang, and Yanzhe Li

## Introduction
We have to develop a chess game which is a partisan game. A partisan game is non-impartital combinatorial game.

## Rules for this game
The rules are the same as the standard chess, however there are rules of antichess implied in this game.
1. If the player to move has a legal chess move which captures an opponent’s piece, then the player to move must make a legal chess move      which captures an opponent’s piece.
2. Every single antichess game is a valid chess game (but the reverse is not true).
3. The result (win/lose/draw) of an antichess game is the same as the result of the corresponding chess game.

## Techniques
We use the alpha beta pruning algorithms to determine the best move for the current player side. Also, we evaluates all the valid moves by using a simple function. 

```
f(p) = 200(K-K')
       + 9(Q-Q')
       + 5(R-R')
       + 3(B-B' + N-N')
       + 1(P-P')
       - 0.5(D-D' + S-S' + I-I')
       + 0.1(M-M') + ...
 
KQRBNP = number of kings, queens, rooks, bishops, knights and pawns
D,S,I = doubled, blocked and isolated pawns
M = Mobility (the number of legal moves)
```
**Reference from** https://chessprogramming.wikispaces.com/Evaluation
