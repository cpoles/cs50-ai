import sys
import random

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable, domain in self.domains.items():
            # ensure that variable satisfies unary constraint
            for word in domain.copy():
                if len(word) != variable.length:
                    self.domains[variable].remove(word)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # if x and y do not overlap, return False. No revision was made.
        if (x, y) not in self.crossword.overlaps.keys():
            return False
        else:
            revised = False
            # get indices of the overlaped letters
            ix, iy = self.crossword.overlaps[x, y] 
            # create an empty set to keep the words that satisfy the constraint
            new_domain = set()             
            # check for constraint satisfaction

            for word in self.domains[x].copy():
                for word2 in self.domains[y]:
                    if word[ix] == word2[iy]: # and word != word2: 
                        # constraint satisfied
                        new_domain.add(word)
                        revised = True

            # update x domain                        
            self.domains[x] = new_domain
            return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        if arcs is None:
            # initialise empty queue as list
            arcs = []
            # populate the arcs queue
            for x in self.crossword.variables:
                neighbours = self.crossword.neighbors(x)
                for y in neighbours:
                    arcs.append((x, y))
        
        # queue is not empty
        while arcs:
            # dequeue arc
            x, y = arcs.pop()
            # revise arc
            if self.revise(x, y): # if changes made to x
                # check if x domain is empty
                if not self.domains[x]:
                    return False
                else:
                    # enqueue x neighbours other than y
                    x_neighs = self.crossword.neighbors(x) - {y}
                    for z in x_neighs:
                        arcs.append((z, x))
        
        return True
    

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # every variable in domains must be in assignment
        for var in self.domains:
            if var not in assignment:
                return False
        return True
        

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # validate constraints

        # monitor if word has been assigned to another var
        assigned = []
        
        for var in assignment:
                     
            # check for uniqueness
            if var in assigned:
                return False
            
            # retrieve word
            value = assignment[var]
            # add to assigned
            assigned.append(var)

            # check length consistency
            if var.length != len(value):
                return False
            
            # check for conflicting caracters between var value and neighbor's value
            if self.crossword.neighbors(var) is not None:
                for neigh in self.crossword.neighbors(var):
                    if neigh in assignment:
                        x, y = self.crossword.overlaps[var, neigh]
                        value_neigh = assignment[neigh]
                        if value[x] != value_neigh[y] or value == value_neigh:
                            return False
            
        return True
                    

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # dictionary for counting ruled-out neighbors
        counts = {value: 0 for value in self.domains[var]}
        
        # for each word in var domains
        for value in self.domains[var]:
            # loop through var neighbors
            for neighbor in self.crossword.neighbors(var):
                # get overlap
                x, y = self.crossword.overlaps[var, neighbor]
                # for each word in the neighbors domain,
                # count if it will be ruled out by the constraint
                for word in self.domains[neighbor]:
                    if value[x] != word[y]:
                        counts[value] += 1
        # return list of values ordered by the number of values they rule out for neighbors
        return [value for value, _ in sorted(counts.items(), key=lambda x: x[1])]


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = {var: domain for var, domain in self.domains.items() if var not in assignment}

        # MRV - select the smallest domain
        sorted_unassigned = sorted(unassigned.items(), key=lambda x: len(x[1]))

        if len(sorted_unassigned) == 1:
            return sorted_unassigned[0][0]
        
        # Select the highest degree if there is a tie
        # count the number neighbours for each var
        neighbours = {}
        for var, _ in sorted_unassigned:
            neighbours[var] = len(self.crossword.neighbors(var))
        # abitrarily choosing the first element             
        var, _ = sorted(neighbours.items(), key=lambda x: x[1], reverse=True)[0]

        return var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        # select unassigned variable
        var = self.select_unassigned_variable(assignment)
        # get unassigned variable domain
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
           # self.ac3()
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
            else:
                del assignment[var]
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
