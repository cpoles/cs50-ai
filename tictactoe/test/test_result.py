from tictactoe import result
import pytest

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




def test_result_raises_index_error():
    board = [[EMPTY, X, EMPTY],
             [EMPTY, O, X],
             [X, EMPTY, O]]
    
    action = (0, 1)

    # raise and index error if spot is filled
    with pytest.raises(IndexError) as invalid_action:   
        result(board, action)
    
    assert str(invalid_action.value) == 'Invalid Action'


def test_result_with_action():
    # return new board with action
    # player user O, position 0,0
    boards = [[[EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY]],
                 
              [[EMPTY, X, EMPTY],
               [EMPTY, O, X],
               [X, EMPTY, O]],

               [[EMPTY, X, EMPTY],
                [EMPTY, O, X],
                [X, EMPTY, O]],
                
               [[X, EMPTY, EMPTY],
                [EMPTY, O, EMPTY],
                [EMPTY, EMPTY, EMPTY]]]

    actions = [(2, 1), (0, 0), (1, 0), (2, 2)]
              
    expected = [[[EMPTY, EMPTY, EMPTY],
                 [EMPTY, EMPTY, EMPTY],
                 [EMPTY, X, EMPTY]],
                  
                 [[O, X, EMPTY],
                  [EMPTY, O, X],
                  [X, EMPTY, O]],

                 [[EMPTY, X, EMPTY],
                  [O, O, X],
                  [X, EMPTY, O]],
              
                  
                 [[X, EMPTY, EMPTY],
                  [EMPTY, O, EMPTY],
                  [EMPTY, EMPTY, X]]]
    
    for board, action, exp in zip(boards, actions, expected):
        assert result(board, action) == exp

                 
