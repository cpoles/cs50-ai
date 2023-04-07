# CROSSWORD

<p>Write an AI to generate crossword puzzles.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$ python generate.py data/structure1.txt data/words1.txt output.png
██████████████
███████M████R█
█INTELLIGENCE█
█N█████N████S█
█F██LOGIC███O█
█E█████M████L█
█R███SEARCH█V█
███████X████E█
██████████████
</code></pre></div></div>

<h2 id="background">Background</h2>

<p>How might you go about generating a crossword puzzle? Given the structure of a crossword puzzle (i.e., which squares of the grid are meant to be filled in with a letter), and a list of words to use, the problem becomes one of choosing which words should go in each vertical or horizontal sequence of squares. We can model this sort of problem as a constraint satisfaction problem. Each sequence of squares is one variable, for which we need to decide on its value (which word in the domain of possible words will fill in that sequence). Consider the following crossword puzzle structure.</p>

![Screenshot](./images/structure.png)

<p>In this structure, we have four variables, representing the four words we need to fill into this crossword puzzle (each indicated by a number in the above image). Each variable is defined by four values: the row it begins on (its <code class="language-plaintext highlighter-rouge">i</code> value), the column it begins on (its <code class="language-plaintext highlighter-rouge">j</code> value), the direction of the word (either down or across), and the length of the word. Variable 1, for example, would be a variable represented by a row of <code class="language-plaintext highlighter-rouge">1</code> (assuming <code class="language-plaintext highlighter-rouge">0</code> indexed counting from the top), a column of <code class="language-plaintext highlighter-rouge">1</code> (also assuming <code class="language-plaintext highlighter-rouge">0</code> indexed counting from the left), a direction of <code class="language-plaintext highlighter-rouge">across</code>, and a length of <code class="language-plaintext highlighter-rouge">4</code>.</p>

<p>As with many constraint satisfaction problems, these variables have both unary and binary constraints. The unary constraint on a variable is given by its length. For Variable 1, for instance, the value <code class="language-plaintext highlighter-rouge">BYTE</code> would satisfy the unary constraint, but the value <code class="language-plaintext highlighter-rouge">BIT</code> would not (it has the wrong number of letters). Any values that don’t satisfy a variable’s unary constraints can therefore be removed from the variable’s domain immediately.</p>

<p>The binary constraints on a variable are given by its overlap with neighboring variables. Variable 1 has a single neighbor: Variable 2. Variable 2 has two neighbors: Variable 1 and Variable 3. For each pair of neighboring variables, those variables share an overlap: a single square that is common to them both. We can represent that overlap as the character index in each variable’s word that must be the same character. For example, the overlap between Variable 1 and Variable 2 might be represented as the pair <code class="language-plaintext highlighter-rouge">(1, 0)</code>, meaning that Variable 1’s character at index 1 necessarily must be the same as Variable 2’s character at index 0 (assuming 0-indexing, again). The overlap between Variable 2 and Variable 3 would therefore be represented as the pair <code class="language-plaintext highlighter-rouge">(3, 1)</code>: character 3 of Variable 2’s value must be the same as character 1 of Variable 3’s value.</p>

<p>For this problem, we’ll add the additional constraint that all words must be different: the same word should not be repeated multiple times in the puzzle.</p>

<p>The challenge ahead, then, is write a program to find a satisfying assignment: a different word (from a given vocabulary list) for each variable such that all of the unary and binary constraints are met.</p>



<h2 id="understanding">Understanding</h2>

<p>There are two Python files in this project: <code class="language-plaintext highlighter-rouge">crossword.py</code> and <code class="language-plaintext highlighter-rouge">generate.py</code>. The first has been entirely written for you, the second has some functions that are left for you to implement.</p>

<p>First, let’s take a look at <code class="language-plaintext highlighter-rouge">crossword.py</code>. This file defines two classes, <code class="language-plaintext highlighter-rouge">Variable</code> (to represent a variable in a crossword puzzle) and <code class="language-plaintext highlighter-rouge">Crossword</code> (to represent the puzzle itself).</p>

<p>Notice that to create a <code class="language-plaintext highlighter-rouge">Variable</code>, we must specify four values: its row <code class="language-plaintext highlighter-rouge">i</code>, its column <code class="language-plaintext highlighter-rouge">j</code>, its direction (either the constant <code class="language-plaintext highlighter-rouge">Variable.ACROSS</code> or the constant <code class="language-plaintext highlighter-rouge">Variable.DOWN</code>), and its length.</p>

<p>The <code class="language-plaintext highlighter-rouge">Crossword</code> class requires two values to create a new crossword puzzle: a <code class="language-plaintext highlighter-rouge">structure_file</code> that defines the structure of the puzzle (the <code class="language-plaintext highlighter-rouge">_</code> is used to represent blank cells, any other character represents cells that won’t be filled in) and a <code class="language-plaintext highlighter-rouge">words_file</code> that defines a list of words (one on each line) to use for the vocabulary of the puzzle. Three examples of each of these files can be found in the <code class="language-plaintext highlighter-rouge">data</code> directory of the project, and you’re welcome to create your own as well.</p>

<p>Note in particular, that for any crossword object <code class="language-plaintext highlighter-rouge">crossword</code>, we store the following values:</p>

<ul>
  <li data-marker="*"><code class="language-plaintext highlighter-rouge">crossword.height</code> is an integer representing the height of the crossword puzzle.</li>
  <li data-marker="*"><code class="language-plaintext highlighter-rouge">crossword.width</code> is an integer representing the width of the crossword puzzle.</li>
  <li data-marker="*"><code class="language-plaintext highlighter-rouge">crossword.structure</code> is a 2D list representing the structure of the puzzle. For any valid row <code class="language-plaintext highlighter-rouge">i</code> and column <code class="language-plaintext highlighter-rouge">j</code>, <code class="language-plaintext highlighter-rouge">crossword.structure[i][j]</code> will be <code class="language-plaintext highlighter-rouge">True</code> if the cell is blank (a character must be filled there) and will be <code class="language-plaintext highlighter-rouge">False</code> otherwise (no character is to be filled in that cell).</li>
  <li data-marker="*"><code class="language-plaintext highlighter-rouge">crossword.words</code> is a set of all of the words to draw from when constructing the crossword puzzle.</li>
  <li data-marker="*"><code class="language-plaintext highlighter-rouge">crossword.variables</code> is a set of all of the variables in the puzzle (each is a <code class="language-plaintext highlighter-rouge">Variable</code> object).</li>
  <li data-marker="*"><code class="language-plaintext highlighter-rouge">crossword.overlaps</code> is a dictionary mapping a pair of variables to their overlap. For any two distinct variables <code class="language-plaintext highlighter-rouge">v1</code> and <code class="language-plaintext highlighter-rouge">v2</code>, <code class="language-plaintext highlighter-rouge">crossword.overlaps[v1, v2]</code> will be <code class="language-plaintext highlighter-rouge">None</code> if the two variables have no overlap, and will be a pair of integers <code class="language-plaintext highlighter-rouge">(i, j)</code> if the variables do overlap. The pair <code class="language-plaintext highlighter-rouge">(i, j)</code> should be interpreted to mean that the <code class="language-plaintext highlighter-rouge">i</code>th character of <code class="language-plaintext highlighter-rouge">v1</code>’s value must be the same as the <code class="language-plaintext highlighter-rouge">j</code>th character of <code class="language-plaintext highlighter-rouge">v2</code>’s value.</li>
</ul>

<p>Crossword objects also support a method <code class="language-plaintext highlighter-rouge">neighbors</code> that returns all of the variables that overlap with a given variable. That is to say, <code class="language-plaintext highlighter-rouge">crossword.neighbors(v1)</code> will return a set of all of the variables that are neighbors to the variable <code class="language-plaintext highlighter-rouge">v1</code>.</p>

<p>Next, take a look at <code class="language-plaintext highlighter-rouge">generate.py</code>. Here, we define a class <code class="language-plaintext highlighter-rouge">CrosswordCreator</code> that we’ll use to solve the crossword puzzle. When a <code class="language-plaintext highlighter-rouge">CrosswordCreator</code> object is created, it gets a <code class="language-plaintext highlighter-rouge">crossword</code> property that should be a <code class="language-plaintext highlighter-rouge">Crossword</code> object (and therefore has all of the properties described above). Each <code class="language-plaintext highlighter-rouge">CrosswordCreator</code> object also gets a <code class="language-plaintext highlighter-rouge">domains</code> property: a dictionary that maps variables to a set of possible words the variable might take on as a value. Initially, this set of words is all of the words in our vocabulary, but we’ll soon write functions to restrict these domains.</p>

<p>We’ve also defined some functions for you to help with testing your code: <code class="language-plaintext highlighter-rouge">print</code> will print to the terminal a representation of your crossword puzzle for a given assignment (every assignment, in this function and elsewhere, is a dictionary mapping variables to their corresponding words). <code class="language-plaintext highlighter-rouge">save</code>, meanwhile, will generate an image file corresponding to a given assignment (you’ll need to <code class="language-plaintext highlighter-rouge">pip3 install Pillow</code> if you haven’t already to use this function). <code class="language-plaintext highlighter-rouge">letter_grid</code> is a helper function used by both <code class="language-plaintext highlighter-rouge">print</code> and <code class="language-plaintext highlighter-rouge">save</code> that generates a 2D list of all characters in their appropriate positions for a given assignment: you likely won’t need to call this function yourself, but you’re welcome to if you’d like to.</p>

<p>Finally, notice the <code class="language-plaintext highlighter-rouge">solve</code> function. This function does three things: first, it calls <code class="language-plaintext highlighter-rouge">enforce_node_consistency</code> to enforce node consistency on the crossword puzzle, ensuring that every value in a variable’s domain satisfy the unary constraints. Next, the function calls <code class="language-plaintext highlighter-rouge">ac3</code> to enforce arc consistency, ensuring that binary constraints are satisfied. Finally, the function calls <code class="language-plaintext highlighter-rouge">backtrack</code> on an initially empty assignment (the empty dictionary <code class="language-plaintext highlighter-rouge">dict()</code>) to try to calculate a solution to the problem.</p>

<p>The functions <code class="language-plaintext highlighter-rouge">enforce_node_consistency</code>, <code class="language-plaintext highlighter-rouge">ac3</code>, and <code class="language-plaintext highlighter-rouge">backtrack</code>, though, are not yet implemented (among other functions). That’s where you come in!</p>

<h2 id="specification">Specification</h2>

<div class="alert" data-alert="warning" role="alert"><p>An automated tool assists the staff in enforcing the constraints in the below specification. Your submission will fail if any of these are not handled properly, if you import modules other than those explicitly allowed, or if you modify functions other than as permitted.</p></div>

<p>Complete the implementation of <code class="language-plaintext highlighter-rouge">enforce_node_consistency</code>, <code class="language-plaintext highlighter-rouge">revise</code>, <code class="language-plaintext highlighter-rouge">ac3</code>, <code class="language-plaintext highlighter-rouge">assignment_complete</code>, <code class="language-plaintext highlighter-rouge">consistent</code>, <code class="language-plaintext highlighter-rouge">order_domain_values</code>, <code class="language-plaintext highlighter-rouge">selected_unassigned_variable</code>, and <code class="language-plaintext highlighter-rouge">backtrack</code> in <code class="language-plaintext highlighter-rouge">generate.py</code> so that your AI generates complete crossword puzzles if it is possible to do so.</p>

<p>The <code class="language-plaintext highlighter-rouge">enforce_node_consistency</code> function should update <code class="language-plaintext highlighter-rouge">self.domains</code> such that each variable is node consistent.</p>

<ul>
  <li data-marker="*">Recall that node consistency is achieved when, for every variable, each value in its domain is consistent with the variable’s unary constraints. In the case of a crossword puzzle, this means making sure that every value in a variable’s domain has the same number of letters as the variable’s length.</li>
  <li data-marker="*">To remove a value <code class="language-plaintext highlighter-rouge">x</code> from the domain of a variable <code class="language-plaintext highlighter-rouge">v</code>, since <code class="language-plaintext highlighter-rouge">self.domains</code> is a dictionary mapping variables to sets of values, you can call <code class="language-plaintext highlighter-rouge">self.domains[v].remove(x)</code>.</li>
  <li data-marker="*">No return value is necessary for this function.</li>
</ul>

<p>The <code class="language-plaintext highlighter-rouge">revise</code> function should make the variable <code class="language-plaintext highlighter-rouge">x</code> arc consistent with the variable <code class="language-plaintext highlighter-rouge">y</code>.</p>

<ul>
  <li data-marker="*"><code class="language-plaintext highlighter-rouge">x</code> and <code class="language-plaintext highlighter-rouge">y</code> will both be <code class="language-plaintext highlighter-rouge">Variable</code> objects representing variables in the puzzle.</li>
  <li data-marker="*">Recall that <code class="language-plaintext highlighter-rouge">x</code> is arc consistent with <code class="language-plaintext highlighter-rouge">y</code> when every value in the domain of <code class="language-plaintext highlighter-rouge">x</code> has a possible value in the domain of <code class="language-plaintext highlighter-rouge">y</code> that does not cause a conflict. (A conflict in the context of the crossword puzzle is a square for which two variables disagree on what character value it should take on.)</li>
  <li data-marker="*">To make <code class="language-plaintext highlighter-rouge">x</code> arc consistent with <code class="language-plaintext highlighter-rouge">y</code>, you’ll want to remove any value from the domain of <code class="language-plaintext highlighter-rouge">x</code> that does not have a corresponding possible value in the domain of <code class="language-plaintext highlighter-rouge">y</code>.</li>
  <li data-marker="*">Recall that you can access <code class="language-plaintext highlighter-rouge">self.crossword.overlaps</code> to get the overlap, if any, between two variables.</li>
  <li data-marker="*">The domain of <code class="language-plaintext highlighter-rouge">y</code> should be left unmodified.</li>
  <li data-marker="*">The function should return <code class="language-plaintext highlighter-rouge">True</code> if a revision was made to the domain of <code class="language-plaintext highlighter-rouge">x</code>; it should return <code class="language-plaintext highlighter-rouge">False</code> if no revision was made.</li>
</ul>

<p>The <code class="language-plaintext highlighter-rouge">ac3</code> function should, using the AC3 algorithm, enforce arc consistency on the problem. Recall that arc consistency is achieved when all the values in each variable’s domain satisfy that variable’s binary constraints.</p>

<ul>
  <li data-marker="*">Recall that the AC3 algorithm maintains a queue of arcs to process. This function takes an optional argument called <code class="language-plaintext highlighter-rouge">arcs</code>, representing an initial list of arcs to process. If <code class="language-plaintext highlighter-rouge">arcs</code> is <code class="language-plaintext highlighter-rouge">None</code>, your function should start with an initial queue of all of the arcs in the problem. Otherwise, your algorithm should begin with an initial queue of only the arcs that are in the list <code class="language-plaintext highlighter-rouge">arcs</code> (where each arc is a tuple <code class="language-plaintext highlighter-rouge">(x, y)</code> of a variable <code class="language-plaintext highlighter-rouge">x</code> and a different variable <code class="language-plaintext highlighter-rouge">y</code>).</li>
  <li data-marker="*">Recall that to implement AC3, you’ll revise each arc in the queue one at a time. Any time you make a change to a domain, though, you may need to add additional arcs to your queue to ensure that other arcs stay consistent.</li>
  <li data-marker="*">You may find it helpful to call on the <code class="language-plaintext highlighter-rouge">revise</code> function in your implementation of <code class="language-plaintext highlighter-rouge">ac3</code>.</li>
  <li data-marker="*">If, in the process of enforcing arc consistency, you remove all of the remaining values from a domain, return <code class="language-plaintext highlighter-rouge">False</code> (this means it’s impossible to solve the problem, since there are no more possible values for the variable). Otherwise, return <code class="language-plaintext highlighter-rouge">True</code>.</li>
  <li data-marker="*">You do not need to worry about enforcing word uniqueness in this function (you’ll implement that check in the <code class="language-plaintext highlighter-rouge">consistent</code> function.)</li>
</ul>

<p>The <code class="language-plaintext highlighter-rouge">assignment_complete</code> function should (as the name suggests) check to see if a given <code class="language-plaintext highlighter-rouge">assignment</code> is complete.</p>

<ul>
  <li data-marker="*">An <code class="language-plaintext highlighter-rouge">assignment</code> is a dictionary where the keys are <code class="language-plaintext highlighter-rouge">Variable</code> objects and the values are strings representing the words those variables will take on.</li>
  <li data-marker="*">An assignment is complete if every crossword variable is assigned to a value (regardless of what that value is).</li>
  <li data-marker="*">The function should return <code class="language-plaintext highlighter-rouge">True</code> if the assignment is complete and return <code class="language-plaintext highlighter-rouge">False</code> otherwise.</li>
</ul>

<p>The <code class="language-plaintext highlighter-rouge">consistent</code> function should check to see if a given <code class="language-plaintext highlighter-rouge">assignment</code> is consistent.</p>

<ul>
  <li data-marker="*">An <code class="language-plaintext highlighter-rouge">assignment</code> is a dictionary where the keys are <code class="language-plaintext highlighter-rouge">Variable</code> objects and the values are strings representing the words those variables will take on. Note that the assignment may not be complete: not all variables will necessarily be present in the assignment.</li>
  <li data-marker="*">An assignment is consistent if it satisfies all of the constraints of the problem: that is to say, all values are distinct, every value is the correct length, and there are no conflicts between neighboring variables.</li>
  <li data-marker="*">The function should return <code class="language-plaintext highlighter-rouge">True</code> if the assignment is consistent and return <code class="language-plaintext highlighter-rouge">False</code> otherwise.</li>
</ul>

<p>The <code class="language-plaintext highlighter-rouge">order_domain_values</code> function should return a list of all of the values in the domain of <code class="language-plaintext highlighter-rouge">var</code>, ordered according to the least-constraining values heuristic.</p>

<ul>
  <li data-marker="*"><code class="language-plaintext highlighter-rouge">var</code> will be a <code class="language-plaintext highlighter-rouge">Variable</code> object, representing a variable in the puzzle.</li>
  <li data-marker="*">Recall that the least-constraining values heuristic is computed as the number of values ruled out for neighboring unassigned variables. That is to say, if assigning <code class="language-plaintext highlighter-rouge">var</code> to a particular value results in eliminating <code class="language-plaintext highlighter-rouge">n</code> possible choices for neighboring variables, you should order your results in ascending order of <code class="language-plaintext highlighter-rouge">n</code>.</li>
  <li data-marker="*">Note that any variable present in <code class="language-plaintext highlighter-rouge">assignment</code> already has a value, and therefore shouldn’t be counted when computing the number of values ruled out for neighboring unassigned variables.</li>
  <li data-marker="*">For domain values that eliminate the same number of possible choices for neighboring variables, any ordering is acceptable.</li>
  <li data-marker="*">Recall that you can access <code class="language-plaintext highlighter-rouge">self.crossword.overlaps</code> to get the overlap, if any, between two variables.</li>
  <li data-marker="*">It may be helpful to first implement this function by returning a list of values in any arbitrary order (which should still generate correct crossword puzzles). Once your algorithm is working, you can then go back and ensure that the values are returned in the correct order.</li>
  <li data-marker="*">You may find it helpful to <a href="https://docs.python.org/3/howto/sorting.html"><code class="language-plaintext highlighter-rouge">sort</code></a> a list according to a particular <code class="language-plaintext highlighter-rouge">key</code>: Python contains some helpful functions for achieving this.</li>
</ul>

<p>The <code class="language-plaintext highlighter-rouge">select_unassigned_variable</code> function should return a single variable in the crossword puzzle that is not yet assigned by <code class="language-plaintext highlighter-rouge">assignment</code>, according to the minimum remaining value heuristic and then the degree heuristic.</p>

<ul>
  <li data-marker="*">An <code class="language-plaintext highlighter-rouge">assignment</code> is a dictionary where the keys are <code class="language-plaintext highlighter-rouge">Variable</code> objects and the values are strings representing the words those variables will take on. You may assume that the assignment will not be complete: not all variables will be present in the assignment.</li>
  <li data-marker="*">Your function should return a <code class="language-plaintext highlighter-rouge">Variable</code> object. You should return the variable with the fewest number of remaining values in its domain. If there is a tie between variables, you should choose among whichever among those variables has the largest degree (has the most neighbors). If there is a tie in both cases, you may choose arbitrarily among tied variables.</li>
  <li data-marker="*">It may be helpful to first implement this function by returning any arbitrary unassigned variable (which should still generate correct crossword puzzles). Once your algorithm is working, you can then go back and ensure that you are returning a variable according to the heuristics.</li>
  <li data-marker="*">You may find it helpful to <a href="https://docs.python.org/3/howto/sorting.html"><code class="language-plaintext highlighter-rouge">sort</code></a> a list according to a particular <code class="language-plaintext highlighter-rouge">key</code>: Python contains some helpful functions for achieving this.</li>
</ul>

<p>The <code class="language-plaintext highlighter-rouge">backtrack</code> function should accept a partial assignment <code class="language-plaintext highlighter-rouge">assignment</code> as input and, using backtracking search, return a complete satisfactory assignment of variables to values if it is possible to do so.</p>

<ul>
  <li data-marker="*">An <code class="language-plaintext highlighter-rouge">assignment</code> is a dictionary where the keys are <code class="language-plaintext highlighter-rouge">Variable</code> objects and the values are strings representing the words those variables will take on. The input assignment may not be complete (not all variables will necessarily have values).</li>
  <li data-marker="*">If it is possible to generate a satisfactory crossword puzzle, your function should return the complete assignment: a dictionary where each variable is a key and the value is the word that the variable should take on. If no satisfying assignment is possible, the function should return <code class="language-plaintext highlighter-rouge">None</code>.</li>
  <li data-marker="*">If you would like, you may find that your algorithm is more efficient if you interleave search with inference (as by maintaining arc consistency every time you make a new assignment). You are not required to do this, but you are permitted to, so long as your function still produces correct results. (It is for this reason that the <code class="language-plaintext highlighter-rouge">ac3</code> function allows an <code class="language-plaintext highlighter-rouge">arcs</code> argument, in case you’d like to start with a different queue of arcs.)</li>
</ul>

<p>You should not modify anything else in <code class="language-plaintext highlighter-rouge">generate.py</code> other than the functions the specification calls for you to implement, though you may write additional functions and/or import other Python standard library modules. You may also import <code class="language-plaintext highlighter-rouge">numpy</code> or <code class="language-plaintext highlighter-rouge">pandas</code>, if familiar with them, but you should not use any other third-party Python modules. You should not modify anything in <code class="language-plaintext highlighter-rouge">crossword.py</code>.</p>
