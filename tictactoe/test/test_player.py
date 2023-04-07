from tictactoe import player


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

def test_player_initial_state():
    # X gets first move when board in initial state
    assert player(initial_board) == X


def test_player_game_over_full_board():
    # Return Game Over when board is in terminal state
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
              
    
    expected = [X, O, X, O]

    for board in boards:
        assert player(board) == 'Game Over.'


def test_player_game_over_not_full_board():
    # Return Game Over when board is in terminal state and not full
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
        assert player(board) == 'Game Over.'


def test_player_turn():
    # Return the next player to play
    boards = [[[X, EMPTY, EMPTY],
               [EMPTY, EMPTY, EMPTY],
               [EMPTY, EMPTY, EMPTY]], # return O

              [[X, EMPTY, EMPTY],
               [EMPTY, O, EMPTY],
               [EMPTY, EMPTY, EMPTY]], # return X
                
              [[X, O, O],
               [O, X, O],
               [X, X, EMPTY]], # return X
               
              [[X, EMPTY, EMPTY],
                [O, X, O],
                [X, EMPTY, EMPTY]]] # return O

    outcomes = [O, X, X, O]

    for board, exp in zip(boards, outcomes):
        assert player(board) == exp