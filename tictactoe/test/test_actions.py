from tictactoe import actions

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
    
    
def test_actions_terminal_board():

    for board in terminal_boards:
        assert actions(board) == "Game Over. No more actions allowed."


def test_actions_initial_board():

    # all possible actions when board is at initial state
    expected = {
        (0,0), (0,1), (0,2),
        (1,0), (1,1), (1,2),
        (2,0), (2,1), (2,2)
    }

    assert actions(initial_board) == expected

def test_actions_multiple_boards():

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
                [X, EMPTY, EMPTY]]]
    
    expected = [{(0,1), (0,2), (1,0), (1,1), (1,2),(2,0), (2,1), (2,2)},
                {(0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)},
                {(2,2)},
                {(0,1), (0,2),(2,1), (2,2)}]
    
    for board, exp in zip(boards, expected):
        assert actions(board) == exp