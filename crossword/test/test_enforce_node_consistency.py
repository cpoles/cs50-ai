from generate import CrosswordCreator
from crossword import Variable, Crossword

crossword = Crossword('./data/structure0.txt', './data/words0.txt')
nodeC = CrosswordCreator(crossword)

domain = { Variable(4, 1, 'across', 4): {'FIVE', 'FOUR', 'NINE'}, 
  Variable(0, 1, 'down', 5): {'THREE', 'SEVEN', 'EIGHT'}, 
  Variable(0, 1, 'across', 3): {'ONE', 'SIX', 'TWO', 'TEN'}, 
  Variable(1, 4, 'down', 4): {'FIVE', 'FOUR', 'NINE' } }


def test_enforce_node_consistency():
    nodeC.enforce_node_consistency()
    assert nodeC.domains == domain

