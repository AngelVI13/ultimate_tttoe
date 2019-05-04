import random
import time
from multiprocessing import Queue, Process
from operator import itemgetter

from board.ultimate_board import UltimateBoard as Board
from engine.node import Node


def uct_multi(rootstate_: Board, itermax, verbose):
    moves = rootstate_.get_moves()

    if len(moves) == 1:  # if only 1 move is possible don't bother searching anything
        return moves[0]

    avg_iters = itermax // len(moves)
    queue = Queue()

    processes = []
    for move in moves:
        current_state = rootstate_.__copy__()
        current_state.make_move(*move)
        p = Process(target=uct, args=(queue, move, current_state, avg_iters, verbose))
        p.start()
        processes.append(p)

    for process in processes:
        process.join()
    # for move in moves:
    #     state = rootstate_.__copy__()
    #     state.make_move(*move)
    #     uct(queue, move, state, avg_iters, verbose)
    # time.sleep(0.1)

    results = []
    while not queue.empty():
        move, wins, visits = queue.get()
        results.append((move, wins/visits))

    # the score here refers to the score of the best enemy reply -> we choose a move which leads to a best enemy reply
    # with the least score
    best_move, score = sorted(results, key=itemgetter(1))[0]
    return best_move


def rand_choice(x):  # fastest way to get random item from list
    return x[int(random.random() * len(x))]


def uct(queue: Queue, move_origin, rootstate, itermax, verbose=False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state=rootstate)

    state = rootstate
    for i in range(itermax):
        node = rootnode
        moves_to_root = 0

        # Select
        while not node.untriedMoves and node.childNodes:  # node is fully expanded and non-terminal
            node = node.uct_select_child()
            state.make_move(*node.move)
            moves_to_root += 1

        # Expand
        if node.untriedMoves:  # if we can expand (i.e. state/node is non-terminal)
            m = rand_choice(node.untriedMoves)
            state.make_move(*m)
            moves_to_root += 1
            node = node.add_child(m, state)  # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.get_result(state.playerJustMoved) is None:  # while state is non-terminal
            state.make_move(*rand_choice(state.get_moves()))
            moves_to_root += 1

        # Backpropagate
        while node is not None:  # backpropagate from the expanded node and work back to the root node
            # state is terminal. Update node with result from POV of node.playerJustMoved
            result = state.get_result(node.playerJustMoved)
            node.update(result)
            node = node.parentNode

        for _ in range(moves_to_root):
            state.take_move()

    # Output some information about the tree - can be omitted
    # if verbose:
    #     print(rootnode.convert_tree_to_string(0))
    # else:
    #     print(rootnode.convert_children_to_string())

    # return sorted(rootnode.childNodes, key=lambda c: c.visits)[-1].move  # return the move that was most visited
    bestNode = sorted(rootnode.childNodes, key=lambda c: c.visits)[-1]
    queue.put((move_origin, bestNode.wins, bestNode.visits))


def uct_play_game():
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    state = Board()

    while state.get_result(state.playerJustMoved) is None:
        print(state)
        start = time.time()
        m = uct_multi(rootstate_=state, itermax=50000, verbose=False)  # play with values for itermax and verbose = True
        print('Time it took', time.time() - start)
        print("Best Move: ", m, "\n")
        state.make_move(m)
    print(state)
    if state.get_result(state.playerJustMoved) == 1.0:
        print("Player " + str(state.playerJustMoved) + " wins!")
    elif state.get_result(state.playerJustMoved) == 0.0:
        print("Player " + str(-state.playerJustMoved) + " wins!")
    else:
        print("Nobody wins!")


def user_play():
    state = Board()

    while state.get_result(state.playerJustMoved) is None:
        print(state)
        move = int(input('Enter move:'))
        state.make_move(move)
        print(state)
        start = time.time()
        m = uct_multi(rootstate_=state, itermax=50000, verbose=False)  # play with values for itermax and verbose = True
        print('Time it took', time.time() - start)
        print("Best Move: ", m, "\n")
        state.make_move(m)
    print(state)
    if state.get_result(state.playerJustMoved) == 1.0:
        print("Player " + str(state.playerJustMoved) + " wins!")
    elif state.get_result(state.playerJustMoved) == 0.0:
        print("Player " + str(-state.playerJustMoved) + " wins!")
    else:
        print("Nobody wins!")


if __name__ == "__main__":
    """ Play a single game to the end using UCT for both players. 
    """
    # uct_play_game()
    user_play()
