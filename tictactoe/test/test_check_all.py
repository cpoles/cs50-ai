from tictactoe import check_all

O ='O'
X = 'X'
EMPTY = None

rows = [
    [True, True, True],
    [False, False, False],
    [X, X, X],
    [X, O, EMPTY],
    [O, O, O],
    [True, False, False],
]


outcomes = [True, True, True, False, True, False]

def test_check_all_not_empty():
    # return True if all elements are equal
    for row, expected in zip(rows, outcomes):
        assert check_all(row) == expected


def test_check_all_empty():
    assert check_all([EMPTY, EMPTY, EMPTY]) == False