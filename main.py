import chess

from agents import NegamaxAgent, NegaScoutAgent, PvsAgent
from heuristic import BasicHeuristic, MaterialHeuristic


class Game:
    def __init__(self):
        self.board = chess.Board()

    def makeAgentMove(self):
        agent = PvsAgent(self.board, self.board.turn, 3,
                         MaterialHeuristic(self.board))
        move = agent.getMove()
        self.board.push(move)

    def start(self):
        while not self.board.is_checkmate():
            self.makeAgentMove()
            print(self.board)
            print('\n')


game = Game()
game.start()
