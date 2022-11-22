import chess
import chess.engine
import random
import math

from heuristic import Heuristic
from tree import Node


class Agent:
    def getMove() -> chess.Move:
        raise NotImplementedError()


class MctsAgent(Agent):
    def __init__(self, board: chess.Board, color: chess.Color, heuristic: Heuristic):
        self.board = board
        self.color = color
        self.heuristic = heuristic

    def getMove(self):
        return self.algorithm()

    def algorithm(self):
        searchedChildren = 0
        root = Node(self.board, None, None)

        while searchedChildren < 16:
            leaf = self.getLeaf(root)

            if leaf.unexploredMoves:
                child = self.expand(leaf)
            else:
                child = leaf

            score = self.evaluate(child)
            self.backpropagate(child, score)
            searchedChildren += 1

        move = max(root.children, key=lambda node: node.simulations)

        return move.action

    def getLeaf(self, node: Node):
        maxNode = node
        while (not maxNode.unexploredMoves) and maxNode.children:
            selection = max(maxNode.children, key=self.getUcb)
            node = selection

        return node

    def getUcb(self, node: Node):
        try:
            ucb = (node.simulations - node.wins / node.simulations) + (math.sqrt(2)
                                                                       * math.sqrt(math.log(node.parent.simulations) / node.simulations))
        except ZeroDivisionError:
            ucb = float('inf')

        return ucb

    def expand(self, node: Node):
        move = node.unexploredMoves.pop()
        stateCopy = node.state.copy()
        stateCopy.push(move)
        child = Node(stateCopy, node, move)
        node.children.append(child)

        return child

    def evaluate(self, node: Node):
        return self.simulate(node)

    def simulate(self, node: Node):
        board = node.state.copy()
        while not board.is_game_over():
            move = random.choice(list(board.legal_moves))
            board.push(move)

        return self.heuristic.evaluate(node.state, node.state.turn)

    def backpropagate(self, node: Node, result: int):
        node.wins += result.pov(node.color).expectation()
        node.simulations += 1

        currentNode = node
        while currentNode.parent is not None:
            currentNode.parent.wins += result.pov(
                currentNode.parent.color).expectation()
            currentNode.parent.simulations += 1
            currentNode = currentNode.parent
