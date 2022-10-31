import chess
import chess.svg

from agents import PvsAgent
from heuristic import BasicHeuristic


class Game:
    def __init__(self, board: chess.Board):
        self.board = board

    def makeAgentMove(self,  color):
        agent = PvsAgent(self.board, color, 5,
                         BasicHeuristic(self.board))
        move = agent.getMove()
        self.board.push(move)

    def start(self):
        turn = chess.WHITE

        while (not self.board.is_checkmate()):
            print(self.board)

            if turn == chess.WHITE:
                print('\nWhite move\n')
                self.makeAgentMove(chess.WHITE)
                turn = chess.BLACK
            else:
                print('\nBlack move\n')
                self.makeAgentMove(chess.BLACK)
                turn = chess.WHITE


game = Game(chess.Board())
game.start()
