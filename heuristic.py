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

        score += self.evaluateCheckmate(color)

        return score

    def evaluateCell(self, cell: int, color: chess.Color) -> int:
        piece = self.board.piece_type_at(cell)

        score = 0
        if piece in self.points:
            score = self.points[piece]

        if (self.board.color_at(cell) != color):
            return -score

        return score

    def evaluateCheckmate(self, color: chess.Color):
        if self.board.is_checkmate():
            if (self.board.turn == color):
                return -9999
            else:
                return 9999
        else:
            return 0


class MaterialHeuristic(Heuristic):
    def __init__(self, board: chess.Board):
        self.board = board

    def evaluate(self, color: chess.Color) -> int:
        white = self.board.occupied_co[chess.WHITE]
        black = self.board.occupied_co[chess.BLACK]
        score = self.getMaterialBalance() * (white - black)

        if (self.board.turn != color):
            return -score

        return score

    def getMaterialBalance(self):
        white = self.board.occupied_co[chess.WHITE]
        black = self.board.occupied_co[chess.BLACK]

        return (
            chess.popcount(white & self.board.pawns) -
            chess.popcount(black & self.board.pawns) +
            3 * (chess.popcount(white & self.board.knights) - chess.popcount(black & self.board.knights)) +
            3 * (chess.popcount(white & self.board.bishops) - chess.popcount(black & self.board.bishops)) +
            5 * (chess.popcount(white & self.board.rooks) - chess.popcount(black & self.board.rooks)) +
            9 * (chess.popcount(white & self.board.queens) -
                 chess.popcount(black & self.board.queens))
        )
