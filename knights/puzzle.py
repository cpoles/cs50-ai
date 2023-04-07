from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave), # can be either a knight or a knave
    Not(And(AKnight, AKnave)), # cannot be both at the same time

    Implication(AKnave, Not(And(AKnight, AKnave))), 
    Implication(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave), # A can be either a knight or a knave
    Not(And(AKnight, AKnave)), # A cannot be both at the same time
    Or(BKnight, BKnave), # B can be either a knight or a knave
    Not(And(BKnave, BKnight)), # B cannot be both at the same time

    Implication(AKnave, Not(And(AKnave, BKnave))), # If A is a knave, then they are both knights
    Implication(AKnight, And(AKnave, BKnave))) # If A is a knight, then they are both knaves

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds." 
knowledge2 = And(
    Or(AKnight, AKnave), # A can be either a knight or a knave
    Not(And(AKnight, AKnave)), # A cannot be both at the same time
    Or(BKnight, BKnave), # B can be either a knight or a knave
    Not(And(BKnave, BKnight)), # B cannot be both at the same time

    Implication(AKnight, And(AKnight, BKnight)), # if A is a knight then they are of the same kind
    Implication(AKnave, Not(And(AKnave, BKnave))), # if A is knave then they not of the same kind
    Implication(BKnight, And(BKnight, AKnave)), # if B is a knight then they are of different kinds
    Implication(BKnave, Not(And(BKnave, AKnight))) # if B is a knave then they are not of different kinds
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave), # A can be either a knight or a knave
    Not(And(AKnight, AKnave)), # A cannot be both at the same time

    Or(BKnight, BKnave), # B can be either a knight or a knave
    Not(And(BKnave, BKnight)), # B cannot be both at the same time

    Or(CKnight, CKnave), # C can be either a knight or a knave
    Not(And(CKnave, CKnight)), # C cannot be both at the same time

    # if B is a knight, A said B is a knave
    # then A can be either a knight or a knave
    Implication(BKnight, 
                And(Implication(AKnight, AKnave), 
                    Implication(AKnave, Not(AKnave)))),
    
    # if B is a knave, A said B is not a knave
    # then A can be either a knight or a knave
    Implication(BKnave, 
                Not(And(Implication(AKnight, AKnave), 
                        Implication(AKnave, Not(AKnave))))),

    Implication(BKnight, CKnave), # if B is knight then C is a knave
    Implication(BKnave, Not(CKnave)), # if B is a nave then C is a not a knave
    
    Implication(CKnight, AKnight), # if C is knight then A is a knight
    Implication(CKnave, Not(AKnight)) # if C is knave then C is a knave
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
