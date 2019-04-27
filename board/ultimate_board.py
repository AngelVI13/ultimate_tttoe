import random
from collections import deque, namedtuple
from typing import List, Tuple

from board.base_board import *


Move = namedtuple('Move', ['board_idx', 'move_idx'])


class UltimateBoard(BaseBoard):
    """Board implementation for ultimate tic tac toe. Supports any NxN size board."""

    def __init__(self):
        self.pos = [Board() for _ in range(BOARD_SIZE)]
        # indicates where (which board) the next move should be done
        self.nextBoard = None
        self.playerJustMoved = PLAYER_O
        self.history = deque()

    def __str__(self):
        lines = []
        for combo in zip(*[self.pos[i::ROWS] for i in range(ROWS)]):
            rows = zip(*[elem.get_row_strings() for elem in combo])
            row = [''.join(['\t|\t'.join(row), '\n']) for row in rows]
            row_length = sum([len(r) for r in row]) // ROWS
            lines.extend(row)
            lines.append(''.join(['_'*row_length, '\n']))
        return ''.join(lines)

    def __copy__(self):
        _b = UltimateBoard()
        _b.pos = [board.__copy__() for board in self.pos]
        _b.nextBoard = self.nextBoard
        _b.playerJustMoved = self.playerJustMoved
        _b.history = self.history.copy()
        return _b

    def make_move(self, move: int, board: int = None):
        """Make a move to the specified board, if no board is specified
        the move is done on the board indicated by nextBoard i.e forced
        by the last played move.

        @param move: move to play (i.e. index on the board)
        @param board: index indicating which board to play the move on
        """
        self.playerJustMoved = -self.playerJustMoved

        if self.nextBoard is None and board is None:
            print('Need to provide a board idx at start of game')
            return

        if self.nextBoard is not None:
            # if we are forced to play on a board (due to opponents move)
            # check if nextBoard has a winner. If it does => player should
            # have picked a new board to play on
            if self.pos[self.nextBoard].get_result() is not None:
                if board is None:
                    print('The forced board already has a result on it.'
                          'Please choose a different board.')
                    return
                else:
                    if self.pos[board].get_result() is not None:
                        print('The chosen board has a result on it.'
                              'Please chose a different board.')
                        return

                    self.pos[board].make_move(move, self.playerJustMoved)
                    self.history.append(Move(board_idx=board, move_idx=move))
                    # todo if nextBoard points to a board that is already final => nextBoard could be all available boards
                    self.nextBoard = move  # the move on the board represents the next board
                    return

            # otherwise the forced board, doesn't have a result and the new move
            # must be played on it
            self.pos[self.nextBoard].make_move(move, self.playerJustMoved)
            self.history.append(Move(board_idx=self.nextBoard, move_idx=move))
            # todo if nextBoard points to a board that is already final => nextBoard could be all available boards
            self.nextBoard = move
            return

        # if board is not None but nextBoard is None (i.e. start of game)
        self.pos[board].make_move(move, self.playerJustMoved)
        self.history.append(Move(board_idx=board, move_idx=move))
        # todo if nextBoard points to a board that is already final => nextBoard could be all available boards
        self.nextBoard = move

    def take_move(self):
        move = self.history.pop()
        self.pos[move.board_idx].take_move(move.move_idx)
        # todo if nextBoard points to a board that is already final => nextBoard could be all available boards
        self.nextBoard = move.board_idx  # update nextBoard to be the one forced

    def get_all_moves(self) -> List[Tuple[int, int]]:
        """Get all possible moves in the form of a list of tuples
        containing (Board index, Move index).
        """
        all_moves = []
        for idx, board in enumerate(self.pos):
            if board.get_result() is not None:
                continue

            moves = board.get_moves()
            if moves:
                all_moves.extend(zip([idx]*len(moves), moves))
        return all_moves

    def get_moves(self):
        """If a board is forced, return only the moves from that board.
        If a board is forced but that board already has a result,
        return all possible moves from all the other boards. If no
        board is forced, return all possible moves.
        """
        # at the start of the game return all possible moves
        if self.nextBoard is None:
            return self.get_all_moves()

        # if a forced board has a result -> return list of moves for
        # all other boards that do not yet have a result
        if self.pos[self.nextBoard].get_result() is not None:
            all_moves = []
            for idx, board in enumerate(self.pos):
                if idx != self.nextBoard and board.get_result() is None:
                    moves = board.get_moves()
                    if moves:
                        all_moves.extend(zip([idx] * len(moves), moves))
            return all_moves

        # if forced board doesn't have a result yet => get all possible moves
        # from that board
        all_moves = []
        moves = self.pos[self.nextBoard].get_moves()
        if moves:
            all_moves.extend(zip([self.nextBoard] * len(moves), moves))

        return all_moves

    def get_result(self, player_jm):
        # build a list containing the results from each individual board
        # where there is no result i.e. None => replace with 0
        result_board = [board.get_result() for board in self.pos]
        result_board = [0 if result is None else result for result in result_board]

        # find the result based on the result board
        # (use an arbitrary instance of Board() to compute the result)
        result = self.pos[0].get_result(board=result_board)

        if result not in (self.playerJustMoved, -self.playerJustMoved) and not self.get_all_moves():
            # if there is no winner and no available moves => DRAW
            return DRAW
        elif result in (self.playerJustMoved, -self.playerJustMoved):
            return WIN if result == player_jm else LOSS


if __name__ == '__main__':
    ub = UltimateBoard()
    print(ub)
    print('\n\n')
    player = -ub.playerJustMoved
    while ub.get_result(ub.playerJustMoved) is None:
        moves_list = ub.get_moves()
        target_board, move_idx = random.choice(moves_list)
        print(target_board, move_idx)
        ub.make_move(move_idx, target_board)
        print(ub)
        print('\n\n')

    print('Game finished. Result is', ub.get_result(player))
