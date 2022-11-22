import chess
import random


class Node:
    state: chess.Board

    parent: 'Node'

    action: chess.Move

    unexploredMoves: list['chess.Move']

    color: chess.Color

    children: list['Node']

    wins: int

    simulations: int

    def __init__(self, state: chess.Board, parent: 'Node', action: chess.Move):
        self.state = state
        self.parent = parent
        self.action = action

        self.unexploredMoves = list(self.state.legal_moves)
        random.shuffle(self.unexploredMoves)
        self.color = self.state.turn
        self.children = []

        self.wins = 0
        self.simulations = 0
