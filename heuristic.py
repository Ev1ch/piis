import chess


class Heuristic:
    def evaluate(self, color: chess.Color) -> int:
        raise NotImplementedError()


class BasicHeuristic(Heuristic):
    def __init__(self, board: chess.Board):
        self.board = board
        self.points = {
            chess.PAWN: 1,
            chess.BISHOP: 3,
            chess.KNIGHT: 4,
            chess.ROOK: 5,
            chess.QUEEN: 8
        }

    def evaluate(self, color: chess.Color) -> int:
        score = 0

        for i in range(64):
            score += self.evaluateCell(chess.SQUARES[i], color)

        return score

    def evaluateCell(self, cell: int, color: chess.Color) -> int:
        piece = self.board.piece_type_at(cell)

        score = 0
        if piece in self.points:
            score = self.points[piece]

        if (self.board.color_at(cell) != color):
            return -score

        return score
