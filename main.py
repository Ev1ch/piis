import chess
import chess.svg
from agents import PvsAgent
from euristics import BasicEuristic


class Game:
    def __init__(self, board: chess.Board):
        self.board = board

    def playAIMove(self,  color):
        engine = PvsAgent(self.board, color, 2,
                          BasicEuristic(self.board))
        bestMove = engine.getMove()
        print('BEST MOVE', bestMove)
        self.board.push(bestMove)

    def start(self):
        # aiColor = chess.BLACK
        print("The game started!")
        # print("You play WHITE!")
        turn = chess.WHITE

        while (not self.board.is_checkmate()):
            print(self.board)

            if turn == chess.WHITE:
                print('\n\nWhite move\n\n')
                self.playAIMove(chess.WHITE)
                turn = chess.BLACK
            else:
                print('\n\nBlack move\n\n')
                self.playAIMove(chess.BLACK)
                turn = chess.WHITE


game = Game(chess.Board())
game.start()
