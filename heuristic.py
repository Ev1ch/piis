import chess
import chess.engine


class Heuristic:
    @staticmethod
    def evaluate(self, board: chess.Board, color: chess.Color) -> chess.engine.PovWdl:
        raise NotImplementedError()


class StaticHeuristic(Heuristic):
    @staticmethod
    def evaluate(board: chess.Board, color: chess.Color):
        score = board.result(claim_draw=True)

        if score == '1-0':
            wdl = chess.engine.Wdl(wins=1000, draws=0, losses=0)
        elif score == '0-1':
            wdl = chess.engine.Wdl(wins=0, draws=0, losses=1000)
        else:
            wdl = chess.engine.Wdl(wins=0, draws=1000, losses=0)

        return chess.engine.PovWdl(wdl, color)
