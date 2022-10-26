import chess
import chess.svg


class Agent:
    def __init__(self, board: chess.Board, color: chess.Color):
        raise NotImplementedError()

    def evaluate(self):
        raise NotImplementedError()

    def algorithm(self):
        raise NotImplementedError()

    def getMove():
        raise NotImplementedError()


class NegamaxAgent(Agent):
    def __init__(self, board: chess.Board, color: chess.Color, depth: int):
        self.board = board
        self.color = color
        self.depth = depth

    def evaluate(self):
        score = 0

        for i in range(64):
            score += self.evaluateCell(chess.SQUARES[i])

        return score

    def evaluateCell(self, cell: int):
        pieceCost = 0
        pieceType = self.board.piece_type_at(cell)

        if (pieceType == chess.PAWN):
            pieceCost = 1
        if (pieceType == chess.ROOK):
            pieceCost = 5.1
        if (pieceType == chess.BISHOP):
            pieceCost = 3.33
        if (pieceType == chess.KNIGHT):
            pieceCost = 3.2
        if (pieceType == chess.QUEEN):
            pieceCost = 8.8

        if (self.board.color_at(cell) != self.color):
            return -pieceCost

        return pieceCost

    def getMove(self):
        maxMove = None
        max = float('-inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.algorithm(self.depth)
            self.board.pop()

            if score > max:
                max = score
                maxMove = move

        return maxMove

    def algorithm(self, depth):
        if depth == 0:
            return self.evaluate()

        max = float('-inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.algorithm(depth - 1)
            self.board.pop()

            if score > max:
                max = score

        return max


class GameEngine:
    def __init__(self, board: chess.Board):
        self.board = board

    def playHumanMove(self):
        print("Possible moves: ", self.board.legal_moves)
        play = input("Enter your move: ")

        self.board.push_san(play)

    def playAIMove(self, maxDepth, color, method):
        engine = NegamaxAgent(self.board, color, maxDepth)
        bestMove = engine.getMove()
        print('BEST MOVE', bestMove)
        self.board.push(bestMove)
        return

    def startGame(self, method):
        aiColor = chess.BLACK
        print("The game started!")
        print("You play WHITE!")
        maxDepth = 2
        turn = chess.WHITE
        while (not self.board.is_checkmate()):
            print(self.board)
            if turn == chess.WHITE:
                print('\n\nWhite move\n\n')
                self.playHumanMove()
                turn = chess.BLACK
                continue
            if turn == chess.BLACK:
                print('\n\nBlack move\n\n')
                self.playAIMove(maxDepth, aiColor, method)
                turn = chess.WHITE
                continue
        return


game = GameEngine(chess.Board())

# print("Possible methods: negamax, negascout, vps. negamax is default")

method = ""
method = method if method else "negamax"

# if method != "negamax" and method != "negascout" and method != "vps":
#     print("Wrong method")
#     exit()

# print("You choosed method", method)
game.startGame(method)
