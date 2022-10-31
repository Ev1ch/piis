import chess
from euristics import Euristic


class Agent:
    def getMove() -> chess.Move:
        raise NotImplementedError()


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

        bSearchPv = True
        for move in self.board.legal_moves:
            self.board.push(move)

            if bSearchPv:
                score = -self.algorithm(depth + 1, -beta, -alpha)
            else:
                score = -self.algorithm(depth + 1, -alpha - 1, -alpha)

                if score > alpha and score < beta:
                    score = -self.algorithm(depth + 1, -beta, -alpha)

            self.board.pop()

            if (score >= beta):
                return beta

            if (score > alpha):
                alpha = score
                bSearchPv = False

        return alpha
