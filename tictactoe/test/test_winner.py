from tictactoe import winner


O ='O'
X = 'X'
EMPTY = None

initial_board = [[EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]


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
                   
                   ]


def test_winner_main_diagonal_not_full():
    # Test winner main diagonal with board not full
    boards =  [[[EMPTY, X, X],
                [EMPTY, X, O],
                [X, O, O]], # return X

                [[EMPTY, O, O],
                [EMPTY, O, X],
                [O, X, X]]] # return O 


    outcomes = [X, O]
    
    for board, exp in zip(boards, outcomes):
        assert winner(board) == exp
    
def test_winner_main_diagonal_full():
    # test winner main diagonal with board full
    boards = [[[X, O, O],
               [O, X, O],
               [X, O, X]],

              [[O, O, X],
               [O, O, X],
               [X, O, O]]]

    outcomes = [X, O]

    for board, exp in zip(boards, outcomes):
        assert winner(board) == exp


def test_winner_sec_diagonal_not_full():
    # test winner sec diagonal with board not full
    boards = [[[X, EMPTY, O],
              [EMPTY, O, X],
              [O, EMPTY, X]],

              [[O, EMPTY, X],
               [EMPTY, X, O],
               [X, EMPTY, O]]]

    outcomes = [O, X]

    for board, exp in zip(boards, outcomes):
        assert winner(board) == exp


def test_winner_sec_diagonal_full():
    # test winner sec diagonal with board full
    boards = [[[X, O, O],
               [O, O, X],
               [O, X, X]],
               
               [[X, O, X],
               [O, X, X],
               [X, O, O]]]
    
    outcomes = [O, X]

    for board, exp in zip(boards, outcomes):
        assert winner(board) == exp


def test_winner_horizontal_full():
    # test winner horizontal with board full
    boards = [[[X, O, X],
               [O, O, O],
               [X, X, O]], # O 2nd row

               [[O, O, O],
                [X, O, X],
                [X, X, O]], # O 1st row

               [[O, X, X],
                [X, X, O],
                [O, O, O]]] # 3rd row
    
    outcomes = [O, O, O]

    for board, exp in zip(boards, outcomes):
        assert winner(board) == exp



def test_winner_horizontal_not_full():
    # test winner horizontal with board not full
    boards = [[[X, O, X],
               [O, O, O],
               [EMPTY, X, EMPTY]], # O 2nd row

               [[O, O, O],
                [X, O, X],
               [EMPTY, X, EMPTY]], # O 1st row

               [[EMPTY, X, EMPTY],
                [X, O, X],
                [O, O, O]]] # 3rd row
    
    outcomes = [O, O, O]

    for board, exp in zip(boards, outcomes):
        assert winner(board) == exp
 

def test_winner_vertical_not_full():
    # test winner vertical with board not full
    boards = [[[X, O, O],
               [X, EMPTY, O],
               [X, O, X]], # X 1s column

               [[O, X, O],
                [EMPTY, X, O],
                [O, X, X]], # X 2nd column

                [[O, O, X],
                [EMPTY, O, X],
                [O, X, X]]] # X 3rd column
    
    outcomes = [X, X, X]

    for board, exp in zip(boards, outcomes):
        assert winner(board) == exp


def test_winner_vertical_full():
    # test winner vertical with board full
    boards = [[[X, O, O],
               [X, X, O],
               [X, O, X]], # X 1s column

               [[O, X, O],
                [X, X, O],
                [O, X, X]], # X 2nd column

                [[O, O, X],
                [X, O, X],
                [O, X, X]]] # X 3rd column
    
    for board in boards:
        assert winner(board) == X


def test_winner_no_winner_ful():
    # test no winner with board full
    boards = [[[X, O, O],
              [O, X, X],
              [O, X, O]],

             [[O, X, O],
              [X, O, O],
              [X, O, X]],

             [[O, O, X],
              [X, X, O],
              [O, O, X]]]
    
    for board in boards:
        assert winner(board) == 'No winner'
    

def test_winner_no_winner_not_full():
    # test no winner with board full
    boards = [[[EMPTY, O, EMPTY],
               [O, X, X],
               [O, X, O]],

              [[O, X, EMPTY],
               [X, O, O],
               [EMPTY, O, X]],

              [[O, O, EMPTY],
               [X, X, O],
               [O, EMPTY, X]], 

              [[EMPTY, EMPTY, EMPTY],
               [EMPTY, EMPTY, EMPTY],
               [EMPTY, EMPTY, EMPTY]]]
    
    for board in boards:
        assert winner(board) == 'No winner'

