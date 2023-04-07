# Minesweeper
<h2 id="background">Background</h2>



<p>Minesweeper is a puzzle game that consists of a grid of cells, where some of the cells contain hidden “mines.” Clicking on a cell that contains a mine detonates the mine, and causes the user to lose the game. Clicking on a “safe” cell (i.e., a cell that does not contain a mine) reveals a number that indicates how many neighboring cells – where a neighbor is a cell that is one square to the left, right, up, down, or diagonal from the given cell – contain a mine.</p>

<p>In this 3x3 Minesweeper game, for example, the three <code class="language-plaintext highlighter-rouge">1</code> values indicate that each of those cells has one neighboring cell that is a mine. The four <code class="language-plaintext highlighter-rouge">0</code> values indicate that each of those cells has no neighboring mine.</p>

<p>Given this information, a logical player could conclude that there must be a mine in the lower-right cell and that there is no mine in the upper-left cell, for only in that case would the numerical labels on each of the other cells be accurate.</p>

<p>The goal of the game is to flag (i.e., identify) each of the mines. In many implementations of the game, including the one in this project, the player can flag a mine by right-clicking on a cell (or two-finger clicking, depending on the computer).</p>

### Propositional Logic

<p>Your goal in this project will be to build an AI that can play Minesweeper. Recall that knowledge-based agents make decisions by considering their knowledge base, and making inferences based on that knowledge.</p>

<p>One way we could represent an AI’s knowledge about a Minesweeper game is by making each cell a propositional variable that is true if the cell contains a mine, and false otherwise.</p>

<p>What information does the AI have access to? Well, the AI would know every time a safe cell is clicked on and would get to see the number for that cell. Consider the following Minesweeper board, where the middle cell has been revealed, and the other cells have been labeled with an identifying letter for the sake of discussion.</p>



<p>What information do we have now? It appears we now know that one of the eight neighboring cells is a mine. Therefore, we could write a logical expression like the below to indicate that one of the neighboring cells is a mine.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>Or(A, B, C, D, E, F, G, H)
</code></pre></div></div>

<p>But we actually know more than what this expression says. The above logical sentence expresses the idea that at least one of those eight variables is true. But we can make a stronger statement than that: we know that <strong><em>exactly</em></strong> one of the eight variables is true. This gives us a propositional logic sentence like the below.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>Or(
    And(A, Not(B), Not(C), Not(D), Not(E), Not(F), Not(G), Not(H)),
    And(Not(A), B, Not(C), Not(D), Not(E), Not(F), Not(G), Not(H)),
    And(Not(A), Not(B), C, Not(D), Not(E), Not(F), Not(G), Not(H)),
    And(Not(A), Not(B), Not(C), D, Not(E), Not(F), Not(G), Not(H)),
    And(Not(A), Not(B), Not(C), Not(D), E, Not(F), Not(G), Not(H)),
    And(Not(A), Not(B), Not(C), Not(D), Not(E), F, Not(G), Not(H)),
    And(Not(A), Not(B), Not(C), Not(D), Not(E), Not(F), G, Not(H)),
    And(Not(A), Not(B), Not(C), Not(D), Not(E), Not(F), Not(G), H)
)
</code></pre></div></div>

<p>That’s quite a complicated expression! And that’s just to express what it means for a cell to have a <code class="language-plaintext highlighter-rouge">1</code> in it. If a cell has a <code class="language-plaintext highlighter-rouge">2</code> or <code class="language-plaintext highlighter-rouge">3</code> or some other value, the expression could be even longer.</p>

<p>Trying to perform model checking on this type of problem, too, would quickly become intractable: on an 8x8 grid, the size Microsoft uses for its Beginner level, we’d have 64 variables, and therefore 2^64 possible models to check – far too many for a computer to compute in any reasonable amount of time. We need a better representation of knowledge for this problem.</p>

<h3 id="knowledge-representation">Knowledge Representation</h3>

<p>Instead, we’ll represent each sentence of our AI’s knowledge like the below.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>{A, B, C, D, E, F, G, H} = 1
</code></pre></div></div>

<p>Every logical sentence in this representation has two parts: a set of <code class="language-plaintext highlighter-rouge">cells</code> on the board that are involved in the sentence, and a number <code class="language-plaintext highlighter-rouge">count</code>, representing the count of how many of those cells are mines. The above logical sentence says that out of cells A, B, C, D, E, F, G, and H, exactly 1 of them is a mine.</p>

<p>Why is this a useful representation? In part, it lends itself well to certain types of inference. Consider the game below.</p>



<p>Using the knowledge from the lower-left number, we could construct the sentence <code class="language-plaintext highlighter-rouge">{D, E, G} = 0</code> to mean that out of cells D, E, and G, exactly 0 of them are mines. Intuitively, we can infer from that sentence that all of the cells must be safe. By extension, any time we have a sentence whose <code class="language-plaintext highlighter-rouge">count</code> is <code class="language-plaintext highlighter-rouge">0</code>, we know that all of that sentence’s <code class="language-plaintext highlighter-rouge">cells</code> must be safe.</p>

<p>Similarly, consider the game below.</p>



<p>Our AI would construct the sentence <code class="language-plaintext highlighter-rouge">{E, F, H} = 3</code>. Intuitively, we can infer that all of E, F, and H are mines. More generally, any time the number of <code class="language-plaintext highlighter-rouge">cells</code> is equal to the <code class="language-plaintext highlighter-rouge">count</code>, we know that all of that sentence’s <code class="language-plaintext highlighter-rouge">cells</code> must be mines.</p>

<p>In general, we’ll only want our sentences to be about <code class="language-plaintext highlighter-rouge">cells</code> that are not yet known to be either safe or mines. This means that, once we know whether a cell is a mine or not, we can update our sentences to simplify them and potentially draw new conclusions.</p>

<p>For example, if our AI knew the sentence <code class="language-plaintext highlighter-rouge">{A, B, C} = 2</code>, we don’t yet have enough information to conclude anything. But if we were told that C were safe, we could remove <code class="language-plaintext highlighter-rouge">C</code> from the sentence altogether, leaving us with the sentence <code class="language-plaintext highlighter-rouge">{A, B} = 2</code> (which, incidentally, does let us draw some new conclusions.)</p>

<p>Likewise, if our AI knew the sentence <code class="language-plaintext highlighter-rouge">{A, B, C} = 2</code>, and we were told that C is a mine, we could remove <code class="language-plaintext highlighter-rouge">C</code> from the sentence and decrease the value of <code class="language-plaintext highlighter-rouge">count</code> (since C was a mine that contributed to that count), giving us the sentence <code class="language-plaintext highlighter-rouge">{A, B} = 1</code>. This is logical: if two out of A, B, and C are mines, and we know that C is a mine, then it must be the case that out of A and B, exactly one of them is a mine.</p>

<p>If we’re being even more clever, there’s one final type of inference we can do.</p>



<p>Consider just the two sentences our AI would know based on the top middle cell and the bottom middle cell. From the top middle cell, we have <code class="language-plaintext highlighter-rouge">{A, B, C} = 1</code>. From the bottom middle cell, we have <code class="language-plaintext highlighter-rouge">{A, B, C, D, E} = 2</code>. Logically, we could then infer a new piece of knowledge, that <code class="language-plaintext highlighter-rouge">{D, E} = 1</code>. After all, if two of A, B, C, D, and E are mines, and only one of A, B, and C are mines, then it stands to reason that exactly one of D and E must be the other mine.</p>

<p>More generally, any time we have two sentences <code class="language-plaintext highlighter-rouge">set1 = count1</code> and <code class="language-plaintext highlighter-rouge">set2 = count2</code> where <code class="language-plaintext highlighter-rouge">set1</code> is a subset of <code class="language-plaintext highlighter-rouge">set2</code>, then we can construct the new sentence <code class="language-plaintext highlighter-rouge">set2 - set1 = count2 - count1</code>. Consider the example above to ensure you understand why that’s true.</p>

<p>So using this method of representing knowledge, we can write an AI agent that can gather knowledge about the Minesweeper board, and hopefully select cells it knows to be safe!</p>



<h2 id="understanding">Understanding</h2>

<p>There are two main files in this project: <code class="language-plaintext highlighter-rouge">runner.py</code> and <code class="language-plaintext highlighter-rouge">minesweeper.py</code>. <code class="language-plaintext highlighter-rouge">minesweeper.py</code> contains all of the logic the game itself and for the AI to play the game. <code class="language-plaintext highlighter-rouge">runner.py</code> has been implemented for you, and contains all of the code to run the graphical interface for the game. Once you’ve completed all the required functions in <code class="language-plaintext highlighter-rouge">minesweeper.py</code>, you should be able to run <code class="language-plaintext highlighter-rouge">python runner.py</code> to play Minesweeper (or let your AI play for you)!</p>

<p>Let’s open up <code class="language-plaintext highlighter-rouge">minesweeper.py</code> to understand what’s provided. There are three classes defined in this file, <code class="language-plaintext highlighter-rouge">Minesweeper</code>, which handles the gameplay; <code class="language-plaintext highlighter-rouge">Sentence</code>, which represents a logical sentence that contains both a set of <code class="language-plaintext highlighter-rouge">cells</code> and a <code class="language-plaintext highlighter-rouge">count</code>; and <code class="language-plaintext highlighter-rouge">MinesweeperAI</code>, which handles inferring which moves to make based on knowledge.</p>

<p>The <code class="language-plaintext highlighter-rouge">Minesweeper</code> class has been entirely implemented for you. Notice that each cell is a pair <code class="language-plaintext highlighter-rouge">(i, j)</code> where <code class="language-plaintext highlighter-rouge">i</code> is the row number (ranging from <code class="language-plaintext highlighter-rouge">0</code> to <code class="language-plaintext highlighter-rouge">height - 1</code>) and <code class="language-plaintext highlighter-rouge">j</code> is the column number (ranging from <code class="language-plaintext highlighter-rouge">0</code> to <code class="language-plaintext highlighter-rouge">width - 1</code>).</p>

<p>The <code class="language-plaintext highlighter-rouge">Sentence</code> class will be used to represent logical sentences of the form described in the Background. Each sentence has a set of <code class="language-plaintext highlighter-rouge">cells</code> within it and a <code class="language-plaintext highlighter-rouge">count</code> of how many of those cells are mines. The class also contains functions <code class="language-plaintext highlighter-rouge">known_mines</code> and <code class="language-plaintext highlighter-rouge">known_safes</code> for determining if any of the cells in the sentence are known to be mines or known to be safe. It also contains functions <code class="language-plaintext highlighter-rouge">mark_mine</code> and <code class="language-plaintext highlighter-rouge">mark_safe</code> to update a sentence in response to new information about a cell.</p>

<p>Finally, the <code class="language-plaintext highlighter-rouge">MinesweeperAI</code> class will implement an AI that can play Minesweeper. The AI class keeps track of a number of values. <code class="language-plaintext highlighter-rouge">self.moves_made</code> contains a set of all cells already clicked on, so the AI knows not to pick those again. <code class="language-plaintext highlighter-rouge">self.mines</code> contains a set of all cells known to be mines. <code class="language-plaintext highlighter-rouge">self.safes</code> contains a set of all cells known to be safe. And <code class="language-plaintext highlighter-rouge">self.knowledge</code> contains a list of all of the <code class="language-plaintext highlighter-rouge">Sentence</code>s that the AI knows to be true.</p>

<p>The <code class="language-plaintext highlighter-rouge">mark_mine</code> function adds a cell to <code class="language-plaintext highlighter-rouge">self.mines</code>, so the AI knows that it is a mine. It also loops over all sentences in the AI’s <code class="language-plaintext highlighter-rouge">knowledge</code> and informs each sentence that the cell is a mine, so that the sentence can update itself accordingly if it contains information about that mine. The <code class="language-plaintext highlighter-rouge">mark_safe</code> function does the same thing, but for safe cells instead.</p>

<p>The remaining functions, <code class="language-plaintext highlighter-rouge">add_knowledge</code>, <code class="language-plaintext highlighter-rouge">make_safe_move</code>, and <code class="language-plaintext highlighter-rouge">make_random_move</code>, are left up to you!</p>

<h2 id="specification">Specification</h2>

<div class="alert" data-alert="warning" role="alert"><p>An automated tool assists the staff in enforcing the constraints in the below specification. Your submission will fail if any of these are not handled properly, if you import modules other than those explicitly allowed, if you hardcode the solution, or if you modify functions other than as permitted.</p></div>

<p>Complete the implementations of the <code class="language-plaintext highlighter-rouge">Sentence</code> class and the <code class="language-plaintext highlighter-rouge">MinesweeperAI</code> class in <code class="language-plaintext highlighter-rouge">minesweeper.py</code>.</p>

<p>In the <code class="language-plaintext highlighter-rouge">Sentence</code> class, complete the implementations of <code class="language-plaintext highlighter-rouge">known_mines</code>, <code class="language-plaintext highlighter-rouge">known_safes</code>, <code class="language-plaintext highlighter-rouge">mark_mine</code>, and <code class="language-plaintext highlighter-rouge">mark_safe</code>.</p>

<ul>
  <li data-marker="*">The <code class="language-plaintext highlighter-rouge">known_mines</code> function should return a set of all of the cells in <code class="language-plaintext highlighter-rouge">self.cells</code> that are known to be mines.</li>
  <li data-marker="*">The <code class="language-plaintext highlighter-rouge">known_safes</code> function should return a set of all the cells in <code class="language-plaintext highlighter-rouge">self.cells</code> that are known to be safe.</li>
  <li data-marker="*">The <code class="language-plaintext highlighter-rouge">mark_mine</code> function should first check to see if <code class="language-plaintext highlighter-rouge">cell</code> is one of the cells included in the sentence.
    <ul>
      <li data-marker="*">If <code class="language-plaintext highlighter-rouge">cell</code> is in the sentence, the function should update the sentence so that <code class="language-plaintext highlighter-rouge">cell</code> is no longer in the sentence, but still represents a logically correct sentence given that <code class="language-plaintext highlighter-rouge">cell</code> is known to be a mine.</li>
      <li data-marker="*">If <code class="language-plaintext highlighter-rouge">cell</code> is not in the sentence, then no action is necessary.</li>
    </ul>
  </li>
  <li data-marker="*">The <code class="language-plaintext highlighter-rouge">mark_safe</code> function should first check to see if <code class="language-plaintext highlighter-rouge">cell</code> is one of the cells included in the sentence.
    <ul>
      <li data-marker="*">If <code class="language-plaintext highlighter-rouge">cell</code> is in the sentence, the function should update the sentence so that <code class="language-plaintext highlighter-rouge">cell</code> is no longer in the sentence, but still represents a logically correct sentence given that <code class="language-plaintext highlighter-rouge">cell</code> is known to be safe.</li>
      <li data-marker="*">If <code class="language-plaintext highlighter-rouge">cell</code> is not in the sentence, then no action is necessary.</li>
    </ul>
  </li>
</ul>

<p>In the <code class="language-plaintext highlighter-rouge">MinesweeperAI</code> class, complete the implementations of <code class="language-plaintext highlighter-rouge">add_knowledge</code>, <code class="language-plaintext highlighter-rouge">make_safe_move</code>, and <code class="language-plaintext highlighter-rouge">make_random_move</code>.</p>

<ul>
  <li data-marker="*"><code class="language-plaintext highlighter-rouge">add_knowledge</code> should accept a <code class="language-plaintext highlighter-rouge">cell</code> (represented as a tuple <code class="language-plaintext highlighter-rouge">(i, j)</code>) and its corresponding <code class="language-plaintext highlighter-rouge">count</code>, and update <code class="language-plaintext highlighter-rouge">self.mines</code>, <code class="language-plaintext highlighter-rouge">self.safes</code>, <code class="language-plaintext highlighter-rouge">self.moves_made</code>, and <code class="language-plaintext highlighter-rouge">self.knowledge</code> with any new information that the AI can infer, given that <code class="language-plaintext highlighter-rouge">cell</code> is known to be a safe cell with <code class="language-plaintext highlighter-rouge">count</code> mines neighboring it.
    <ul>
      <li data-marker="*">The function should mark the <code class="language-plaintext highlighter-rouge">cell</code> as one of the moves made in the game.</li>
      <li data-marker="*">The function should mark the <code class="language-plaintext highlighter-rouge">cell</code> as a safe cell, updating any sentences that contain the <code class="language-plaintext highlighter-rouge">cell</code> as well.</li>
      <li data-marker="*">The function should add a new sentence to the AI’s knowledge base, based on the value of <code class="language-plaintext highlighter-rouge">cell</code> and <code class="language-plaintext highlighter-rouge">count</code>, to indicate that <code class="language-plaintext highlighter-rouge">count</code> of the <code class="language-plaintext highlighter-rouge">cell</code>’s neighbors are mines. Be sure to only include cells whose state is still undetermined in the sentence.</li>
      <li data-marker="*">If, based on any of the sentences in <code class="language-plaintext highlighter-rouge">self.knowledge</code>, new cells can be marked as safe or as mines, then the function should do so.</li>
      <li data-marker="*">If, based on any of the sentences in <code class="language-plaintext highlighter-rouge">self.knowledge</code>, new sentences can be inferred (using the subset method described in the Background), then those sentences should be added to the knowledge base as well.</li>
      <li data-marker="*">Note that any time that you make any change to your AI’s knowledge, it may be possible to draw new inferences that weren’t possible before. Be sure that those new inferences are added to the knowledge base if it is possible to do so.</li>
    </ul>
  </li>
  <li data-marker="*"><code class="language-plaintext highlighter-rouge">make_safe_move</code> should return a move <code class="language-plaintext highlighter-rouge">(i, j)</code> that is known to be safe.
    <ul>
      <li data-marker="*">The move returned must be known to be safe, and not a move already made.</li>
      <li data-marker="*">If no safe move can be guaranteed, the function should return <code class="language-plaintext highlighter-rouge">None</code>.</li>
      <li data-marker="*">The function should not modify <code class="language-plaintext highlighter-rouge">self.moves_made</code>, <code class="language-plaintext highlighter-rouge">self.mines</code>, <code class="language-plaintext highlighter-rouge">self.safes</code>, or <code class="language-plaintext highlighter-rouge">self.knowledge</code>.</li>
    </ul>
  </li>
  <li data-marker="*"><code class="language-plaintext highlighter-rouge">make_random_move</code> should return a random move <code class="language-plaintext highlighter-rouge">(i, j)</code>.
    <ul>
      <li data-marker="*">This function will be called if a safe move is not possible: if the AI doesn’t know where to move, it will choose to move randomly instead.</li>
      <li data-marker="*">The move must not be a move that has already been made.</li>
      <li data-marker="*">The move must not be a move that is known to be a mine.</li>
      <li data-marker="*">If no such moves are possible, the function should return <code class="language-plaintext highlighter-rouge">None</code>.</li>
    </ul>
  </li>
</ul>