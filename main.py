import chess

from agents import MctsAgent
from heuristic import StaticHeuristic


class Game:
    def __init__(self):
        self.board = chess.Board()

    def makeAgentMove(self):
        agent = MctsAgent(self.board, self.board.turn, StaticHeuristic)
        move = agent.getMove()
        self.board.push(move)

    def start(self):
        while not self.board.is_checkmate():
            self.makeAgentMove()
            print(self.board)
            print('\n')


game = Game()
game.start()
