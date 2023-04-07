
# NIM

<p>Write an AI that teaches itself to play Nim through reinforcement learning.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$ python play.py
Playing training game 1
Playing training game 2
Playing training game 3
...
Playing training game 9999
Playing training game 10000
Done training

Piles:
Pile 0: 1
Pile 1: 3
Pile 2: 5
Pile 3: 7

AI's Turn
AI chose to take 1 from pile 2.
</code></pre></div></div>

<h2 id="background">Background</h2>

<p>Recall that in the game Nim, we begin with some number of piles, each with some number of objects. Players take turns: on a player’s turn, the player removes any non-negative number of objects from any one non-empty pile. Whoever removes the last object loses.</p>

<p>There’s some simple strategy you might imagine for this game: if there’s only one pile and three objects left in it, and it’s your turn, your best bet is to remove two of those objects, leaving your opponent with the third and final object to remove. But if there are more piles, the strategy gets considerably more complicated. In this problem, we’ll build an AI to learn the strategy for this game through reinforcement learning. By playing against itself repeatedly and learning from experience, eventually our AI will learn which actions to take and which actions to avoid.</p>

<p>In particular, we’ll use Q-learning for this project. Recall that in Q-learning, we try to learn a reward value (a number) for every <code class="language-plaintext highlighter-rouge">(state, action)</code> pair. An action that loses the game will have a reward of -1, an action that results in the other player losing the game will have a reward of 1, and an action that results in the game continuing has an immediate reward of 0, but will also have some future reward.</p>

<p>How will we represent the states and actions inside of a Python program? A “state” of the Nim game is just the current size of all of the piles. A state, for example, might be <code class="language-plaintext highlighter-rouge">[1, 1, 3, 5]</code>, representing the state with 1 object in pile 0, 1 object in pile 1, 3 objects in pile 2, and 5 objects in pile 3. An “action” in the Nim game will be a pair of integers <code class="language-plaintext highlighter-rouge">(i, j)</code>, representing the action of taking <code class="language-plaintext highlighter-rouge">j</code> objects from pile <code class="language-plaintext highlighter-rouge">i</code>. So the action <code class="language-plaintext highlighter-rouge">(3, 5)</code> represents the action “from pile 3, take away 5 objects.” Applying that action to the state <code class="language-plaintext highlighter-rouge">[1, 1, 3, 5]</code> would result in the new state <code class="language-plaintext highlighter-rouge">[1, 1, 3, 0]</code> (the same state, but with pile 3 now empty).</p>

<p>Recall that the key formula for Q-learning is below. Every time we are in a state <code class="language-plaintext highlighter-rouge">s</code> and take an action <code class="language-plaintext highlighter-rouge">a</code>, we can update the Q-value <code class="language-plaintext highlighter-rouge">Q(s, a)</code> according to:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>Q(s, a) &lt;- Q(s, a) + alpha * (new value estimate - old value estimate)
</code></pre></div></div>

<p>In the above formula, <code class="language-plaintext highlighter-rouge">alpha</code> is the learning rate (how much we value new information compared to information we already have). The <code class="language-plaintext highlighter-rouge">new value estimate</code> represents the sum of the reward received for the current action and the estimate of all the future rewards that the player will receive. The <code class="language-plaintext highlighter-rouge">old value estimate</code> is just the existing value for <code class="language-plaintext highlighter-rouge">Q(s, a)</code>. By applying this formula every time our AI takes a new action, over time our AI will start to learn which actions are better in any state.</p>

<h2 id="understanding">Understanding</h2>

<p>First, open up <code class="language-plaintext highlighter-rouge">nim.py</code>. There are two classes defined in this file (<code class="language-plaintext highlighter-rouge">Nim</code> and <code class="language-plaintext highlighter-rouge">NimAI</code>) along with two functions (<code class="language-plaintext highlighter-rouge">train</code> and <code class="language-plaintext highlighter-rouge">play</code>). <code class="language-plaintext highlighter-rouge">Nim</code>, <code class="language-plaintext highlighter-rouge">train</code>, and <code class="language-plaintext highlighter-rouge">play</code> have already been implemented for you, while <code class="language-plaintext highlighter-rouge">NimAI</code> leaves a few functions left for you to implement.</p>

<p>Take a look at the <code class="language-plaintext highlighter-rouge">Nim</code> class, which defines how a Nim game is played. In the <code class="language-plaintext highlighter-rouge">__init__</code> function, notice that every Nim game needs to keep track of a list of piles, a current player (0 or 1), and the winner of the game (if one exists). The <code class="language-plaintext highlighter-rouge">available_actions</code> function returns a set of all the available actions in a state. For example, <code class="language-plaintext highlighter-rouge">Nim.available_actions([2, 1, 0, 0])</code> returns the set <code class="language-plaintext highlighter-rouge">{(0, 1), (1, 1), (0, 2)}</code>, since the three possible actions are to take either 1 or 2 objects from pile 0, or to take 1 object from pile 1.</p>

<p>The remaining functions are used to define the gameplay: the <code class="language-plaintext highlighter-rouge">other_player</code> function determines who the opponent of a given player is, <code class="language-plaintext highlighter-rouge">switch_player</code> changes the current player to the opposing player, and <code class="language-plaintext highlighter-rouge">move</code> performs an action on the current state and switches the current player to the opposing player.</p>

<p>Next, take a look at the <code class="language-plaintext highlighter-rouge">NimAI</code> class, which defines our AI that will learn to play Nim. Notice that in the <code class="language-plaintext highlighter-rouge">__init__</code> function, we start with an empty <code class="language-plaintext highlighter-rouge">self.q</code> dictionary. The <code class="language-plaintext highlighter-rouge">self.q</code> dictionary will keep track of all of the current Q-values learned by our AI by mapping <code class="language-plaintext highlighter-rouge">(state, action)</code> pairs to a numerical value. As an implementation detail, though we usually represent <code class="language-plaintext highlighter-rouge">state</code> as a list, since lists can’t be used as Python dictionary keys, we’ll instead use a tuple version of the state when getting or setting values in <code class="language-plaintext highlighter-rouge">self.q</code>.</p>

<p>For example, if we wanted to set the Q-value of the state <code class="language-plaintext highlighter-rouge">[0, 0, 0, 2]</code> and the action <code class="language-plaintext highlighter-rouge">(3, 2)</code> to <code class="language-plaintext highlighter-rouge">-1</code>, we would write something like</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>self.q[(0, 0, 0, 2), (3, 2)] = -1
</code></pre></div></div>

<p>Notice, too, that every <code class="language-plaintext highlighter-rouge">NimAI</code> object has an <code class="language-plaintext highlighter-rouge">alpha</code> and <code class="language-plaintext highlighter-rouge">epsilon</code> value that will be used for Q-learning and for action selection, respectively.</p>

<p>The <code class="language-plaintext highlighter-rouge">update</code> function is written for you, and takes as input state <code class="language-plaintext highlighter-rouge">old_state</code>, an action take in that state <code class="language-plaintext highlighter-rouge">action</code>, the resulting state after performing that action <code class="language-plaintext highlighter-rouge">new_state</code>, and an immediate reward for taking that action <code class="language-plaintext highlighter-rouge">reward</code>. The function then performs Q-learning by first getting the current Q-value for the state and action (by calling <code class="language-plaintext highlighter-rouge">get_q_value</code>), determining the best possible future rewards (by calling <code class="language-plaintext highlighter-rouge">best_future_reward</code>), and then using both of those values to update the Q-value (by calling <code class="language-plaintext highlighter-rouge">update_q_value</code>). Those three functions are left to you to implement.</p>

<p>Finally, the last function left unimplemented is the <code class="language-plaintext highlighter-rouge">choose_action</code> function, which selects an action to take in a given state (either greedily, or using the epsilon-greedy algorithm).</p>

<p>The <code class="language-plaintext highlighter-rouge">Nim</code> and <code class="language-plaintext highlighter-rouge">NimAI</code> classes are ultimately used in the <code class="language-plaintext highlighter-rouge">train</code> and <code class="language-plaintext highlighter-rouge">play</code> functions. The <code class="language-plaintext highlighter-rouge">train</code> function trains an AI by running <code class="language-plaintext highlighter-rouge">n</code> simulated games against itself, returning the fully trained AI. The <code class="language-plaintext highlighter-rouge">play</code> function accepts a trained AI as input, and lets a human player play a game of Nim against the AI.</p>

<h2 id="specification">Specification</h2>

<div class="alert" data-alert="warning" role="alert"><p>An automated tool assists the staff in enforcing the constraints in the below specification. Your submission will fail if any of these are not handled properly, if you import modules other than those explicitly allowed, or if you modify functions other than as permitted.</p></div>

<p>Complete the implementation of <code class="language-plaintext highlighter-rouge">get_q_value</code>, <code class="language-plaintext highlighter-rouge">update_q_value</code>, <code class="language-plaintext highlighter-rouge">best_future_reward</code>, and <code class="language-plaintext highlighter-rouge">choose_action</code> in <code class="language-plaintext highlighter-rouge">nim.py</code>. For each of these functions, any time a function accepts a <code class="language-plaintext highlighter-rouge">state</code> as input, you may assume it is a list of integers. Any time a function accepts an <code class="language-plaintext highlighter-rouge">action</code> as input, you may assume it is an integer pair <code class="language-plaintext highlighter-rouge">(i, j)</code> of a pile <code class="language-plaintext highlighter-rouge">i</code> and a number of objects <code class="language-plaintext highlighter-rouge">j</code>.</p>

<p>The <code class="language-plaintext highlighter-rouge">get_q_value</code> function should accept as input a <code class="language-plaintext highlighter-rouge">state</code> and <code class="language-plaintext highlighter-rouge">action</code> and return the corresponding Q-value for that state/action pair.</p>

<ul>
  <li data-marker="*">Recall that Q-values are stored in the dictionary <code class="language-plaintext highlighter-rouge">self.q</code>. The keys of <code class="language-plaintext highlighter-rouge">self.q</code> should be in the form of <code class="language-plaintext highlighter-rouge">(state, action)</code> pairs, where <code class="language-plaintext highlighter-rouge">state</code> is a tuple of all piles sizes in order, and <code class="language-plaintext highlighter-rouge">action</code> is a tuple <code class="language-plaintext highlighter-rouge">(i, j)</code> representing a pile and a number.</li>
  <li data-marker="*">If no Q-value for the state/action pair exists in <code class="language-plaintext highlighter-rouge">self.q</code>, then the function should return <code class="language-plaintext highlighter-rouge">0</code>.</li>
</ul>

<p>The <code class="language-plaintext highlighter-rouge">update_q_value</code> function takes a state <code class="language-plaintext highlighter-rouge">state</code>, an action <code class="language-plaintext highlighter-rouge">action</code>, an existing Q value <code class="language-plaintext highlighter-rouge">old_q</code>, a current reward <code class="language-plaintext highlighter-rouge">reward</code>, and an estimate of future rewards <code class="language-plaintext highlighter-rouge">future_rewards</code>, and updates the Q-value for the state/action pair according to the Q-learning formula.</p>

<ul>
  <li data-marker="*">Recall that the Q-learning formula is: <code class="language-plaintext highlighter-rouge">Q(s, a) &lt;- old value estimate + alpha * (new value estimate - old value estimate)</code></li>
  <li data-marker="*">Recall that <code class="language-plaintext highlighter-rouge">alpha</code> is the learning rate associated with the <code class="language-plaintext highlighter-rouge">NimAI</code> object.</li>
  <li data-marker="*">The old value estimate is just the existing Q-value for the state/action pair. The new value estimate should be the sum of the current reward and the estimated future reward.</li>
</ul>

<p>The <code class="language-plaintext highlighter-rouge">best_future_reward</code> function accepts a <code class="language-plaintext highlighter-rouge">state</code> as input and returns the best possible reward for any available action in that state, according to the data in <code class="language-plaintext highlighter-rouge">self.q</code>.</p>

<ul>
  <li data-marker="*">For any action that doesn’t already exist in <code class="language-plaintext highlighter-rouge">self.q</code> for the given state, you should assume it has a Q-value of 0.</li>
  <li data-marker="*">If no actions are available in the state, you should return 0.</li>
</ul>

<p>The <code class="language-plaintext highlighter-rouge">choose_action</code> function should accept a <code class="language-plaintext highlighter-rouge">state</code> as input (and optionally an <code class="language-plaintext highlighter-rouge">epsilon</code> flag for whether to use the epsilon-greedy algorithm), and return an available action in that state.</p>

<ul>
  <li data-marker="*">If <code class="language-plaintext highlighter-rouge">epsilon</code> is <code class="language-plaintext highlighter-rouge">False</code>, your function should behave greedily and return the best possible action available in that state (i.e., the action that has the highest Q-value, using 0 if no Q-value is known).</li>
  <li data-marker="*">If <code class="language-plaintext highlighter-rouge">epsilon</code> is <code class="language-plaintext highlighter-rouge">True</code>, your function should behave according to the epsilon-greedy algorithm, choosing a random available action with probability <code class="language-plaintext highlighter-rouge">self.epsilon</code> and otherwise choosing the best action available.</li>
  <li data-marker="*">If multiple actions have the same Q-value, any of those options is an acceptable return value.</li>
</ul>



