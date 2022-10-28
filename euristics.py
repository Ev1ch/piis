import chess


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
