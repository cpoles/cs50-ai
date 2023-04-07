from generate import CrosswordCreator
from crossword import Variable, Crossword

crossword = Crossword('./data/structure0.txt', './data/words0.txt')
nodeC = CrosswordCreator(crossword)

assignment_true = {Variable(0, 1, 'across', 3): 'SIX', 
              Variable(0, 1, 'down', 5): 'SEVEN', 
              Variable(4, 1, 'across', 4): 'NINE', 
              Variable(1, 4, 'down', 4): 'FIVE'}

assignment_length = {Variable(0, 1, 'across', 3): 'SIX', 
              Variable(0, 1, 'down', 5): 'TWO', 
              Variable(4, 1, 'across', 4): 'NINE', 
              Variable(1, 4, 'down', 4): {'FIVE', 'NINE'}}

assignment_dist = {Variable(0, 1, 'across', 3): 'SIX', 
              Variable(0, 1, 'down', 5): 'SEVEN', 
              Variable(4, 1, 'across', 4): 'NINE', 
              Variable(1, 4, 'down', 4): 'NINE'}



def test_consistent_length_incorrect():
    nodeC.enforce_node_consistency()
    nodeC.ac3()
    assert nodeC.consistent(assignment_length) == False

def test_consistent_not_all_distinct():
    nodeC.enforce_node_consistency()
    nodeC.ac3()
    assert nodeC.consistent(assignment_dist) == False

def test_consistent_all_consistent():
    nodeC.enforce_node_consistency()
    nodeC.ac3()
    assert nodeC.consistent(assignment_true) == True


