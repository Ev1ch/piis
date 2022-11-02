import chess

from agents import NegamaxAgent, NegaScoutAgent, PvsAgent
from heuristic import BasicHeuristic


class Game:
    def __init__(self):
        self.board = chess.Board()

    def makeAgentMove(self):
        agent = NegamaxAgent(self.board, self.board.turn, 2,
                             BasicHeuristic(self.board))
        move = agent.getMove()
        self.board.push(move)

    def start(self):
        while not self.board.is_checkmate():
            self.makeAgentMove()
            print(self.board)
            print('\n')


game = Game()
game.start()
