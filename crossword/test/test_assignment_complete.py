from generate import CrosswordCreator
from crossword import Variable, Crossword

crossword = Crossword('./data/structure0.txt', './data/words0.txt')
nodeC = CrosswordCreator(crossword)

assignment_true = {Variable(0, 1, 'across', 3): 'SIX', 
              Variable(0, 1, 'down', 5): 'SEVEN', 
              Variable(4, 1, 'across', 4): 'NINE', 
              Variable(1, 4, 'down', 4): 'FIVE'}

assignment_false = {Variable(0, 1, 'across', 3): 'SIX', 
              Variable(0, 1, 'down', 5): 'EIGHT', 
              Variable(4, 1, 'across', 4): 'NINE'}


def test_assignment_complete_false():
    nodeC.enforce_node_consistency()
    nodeC.ac3()
    assert nodeC.assignment_complete(assignment_true) == True


def test_assignment_complete_false():
    nodeC.enforce_node_consistency()
    nodeC.ac3()
    assert nodeC.assignment_complete(assignment_false) == False