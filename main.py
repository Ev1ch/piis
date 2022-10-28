import chess
import chess.svg


class Agent:
    def getMove() -> chess.Move:
        raise NotImplementedError()


class Euristic:
    def evaluate(self, color: chess.Color) -> int:
        raise NotImplementedError()


class BasicEuristic(Euristic):
    def __init__(self, board: chess.Board):
        self.board = board

    def evaluate(self, color: chess.Color) -> int:
        score = 0

        for i in range(64):
            score += self.evaluateCell(chess.SQUARES[i], color)

        return score

    def evaluateCell(self, cell: int, color: chess.Color) -> int:
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

        if (self.board.color_at(cell) != color):
            return -pieceCost

        return pieceCost


class NegamaxAgent(Agent):
    def __init__(self, board: chess.Board, color: chess.Color, depth: int, euristic: Euristic):
        self.board = board
        self.color = color
        self.depth = depth
        self.euristic = euristic

    def getMove(self):
        maxMove = chess.Move.null
        max = float('-inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.algorithm(0)
            self.board.pop()

            if score > max:
                max = score
                maxMove = move

        return maxMove

    def algorithm(self, depth):
        if depth == self.depth:
            return self.euristic.evaluate(self.color)

        max = float('-inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.algorithm(depth + 1)
            self.board.pop()

            if score > max:
                max = score

        return max


class NegaScoutAgent(Agent):
    def __init__(self, board: chess.Board, color: chess.Color, depth: int, euristic: Euristic):
        self.board = board
        self.color = color
        self.depth = depth
        self.euristic = euristic

    def getMove(self):
        maxMove = chess.Move.null
        max = float('-inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.algorithm(0, float('-inf'), float('inf'))
            self.board.pop()

            if score > max:
                max = score
                maxMove = move

        return maxMove

    def algorithm(self, depth, alpha, beta):
        if depth == self.depth:
            return self.euristic.evaluate(self.color)

        a = alpha
        b = beta
        i = 0
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.algorithm(depth + 1, -b, -a)
            self.board.pop()

            if score > alpha and score < beta and depth < self.depth - 1 and i > 0:
                a = -self.algorithm(depth + 1, -beta, -score)

            if score > a:
                a = score

            if a >= beta:
                return a

            b = a + 1
            i += 1

        return a


class PvsAgent(Agent):
    def __init__(self, board: chess.Board, color: chess.Color, depth: int, euristic: Euristic):
        self.board = board
        self.color = color
        self.depth = depth
        self.euristic = euristic

    def getMove(self):
        maxMove = chess.Move.null
        max = float('-inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.algorithm(0, float('-inf'), float('inf'))
            self.board.pop()

            if score > max:
                max = score
                maxMove = move

        return maxMove

    def algorithm(self, depth, alpha, beta):
        if depth == self.depth:
            return self.euristic.evaluate(self.color)

        a = alpha
        b = beta
        i = 0
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.algorithm(depth + 1, -b, -a)
            self.board.pop()

            if score > alpha and score < beta:
                a = -self.algorithm(depth + 1, -beta, -alpha)

            if a >= beta:
                return a

            b = a + 1
            i += 1

        return a


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

# print("Possible methods: negamax, negascout, vps. negamax is default")


# if method != "negamax" and method != "negascout" and method != "vps":
#     print("Wrong method")
#     exit()

# print("You choosed method", method)
game.start()
