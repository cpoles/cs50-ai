from tictactoe import utility 

O ='O'
X = 'X'
EMPTY = None

initial_board = [[EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]


def test_utility_terminal_boards():
    terminal_boards = [
                    [[X, O, O],
                     [X, EMPTY, O],
                     [X, O, X]], # X wins vertically not full

                    [[X, O, X],
                     [O, O, O],
                     [EMPTY, X, EMPTY]], # O wins horizontally not full
                    
                    [[X, O, O],
                     [O, X, O],
                     [X, O, X]], # X wins diagonally full

                    [[X, O, O],
                     [O, O, X],
                     [O, X, X]], # O wins sec diagonally full

                    [[X, O, O],
                     [O, X, X],
                     [O, X, O]], # no winner

                    [[O, X, O],
                     [X, O, O],
                     [X, O, X]]] # no winner

    expected = [1, -1, 1, -1, 0, 0]

    for board, exp in zip(terminal_boards, expected):
        assert utility(board) == exp
   