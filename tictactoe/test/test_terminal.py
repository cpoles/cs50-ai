from tictactoe import terminal

O ='O'
X = 'X'
EMPTY = None

initial_board = [[EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]]

def test_terminal_empty():
    assert terminal(initial_board) == False


def test_terminal_winner_full():

    boards = [[[X, O, O],
               [O, X, O],
               [X, O, X]], # X wins diagonally full
                
              [[X, O, O],
               [O, O, X],
               [O, X, X]], # O wins sec diagonally full
                
              [[X, O, O],
               [O, X, O],
               [X, X, X]], # X wins horizontally full

              [[X, O, O],
               [O, O, X],
               [X, O, X]]] # O wins vertically full
    
    for board in boards:
        assert terminal(board) == True


def test_terminal_winner_not_full():
    boards = [[[X, O, EMPTY],
               [O, X, O],
               [EMPTY, O, X]], # X wins diagonally not full
              
              [[X, O, O],
               [EMPTY, O, X],
               [O, X, EMPTY]], # O wins sec diagonally full
              
              [[X, O, EMPTY],
               [O, EMPTY, O],
               [X, X, X]], # X wins horizontally full

              [[X, O, EMPTY],
               [EMPTY, O, O],
               [X, O, X]]] # O wins vertically full
    
    for board in boards:
        assert terminal(board) == True


def test_terminal_no_winner_full():
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
        assert terminal(board) == True


def test_terminal_no_winner_not_full():
    
    boards = [[[EMPTY, O, EMPTY],
                [O, X, X],
                [O, X, O]],

                [[O, X, EMPTY],
                [X, O, O],
                [EMPTY, O, X]],

                [[EMPTY, O, X],
                [X, X, O],
                [O, EMPTY, X]], 

                [[EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY]]]
    
    for board in boards:
        assert terminal(board) == False



    
