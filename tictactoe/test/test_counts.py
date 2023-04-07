from tictactoe import count_turns

O ='O'
X = 'X'
EMPTY = None

initial_board = [[EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]


boards = [  [[X, O, O],
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

            [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]], # initial board

            [[X, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, O, EMPTY]] ]


counts = [ {X: 4, O: 4},
           {X: 3, O: 4},
           {X: 4, O: 5},
           {X: 4, O: 5},
           {X: 0, O: 0},
           {X: 1, O: 1} ]


def test_multiple_boards():
    for board, count in zip(boards, counts):
        assert count_turns(board) == count
