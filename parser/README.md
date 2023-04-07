# Parser

<p>Write an AI to parse sentences and extract noun phrases.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$ python parser.py
Sentence: Holmes sat.
        S
   _____|___
  NP        VP
  |         |
  N         V
  |         |
holmes     sat

Noun Phrase Chunks
holmes
</code></pre></div></div>


<h2 id="background">Background</h2>

<p>A common task in natural language processing is parsing, the process of determining the structure of a sentence. This is useful for a number of reasons: knowing the structure of a sentence can help a computer to better understand the meaning of the sentence, and it can also help the computer extract information out of a sentence. In particular, it’s often useful to extract noun phrases out of a sentence to get an understanding for what the sentence is about.</p>

<p>In this problem, we’ll use the context-free grammar formalism to parse English sentences to determine their structure. Recall that in a context-free grammar, we repeatedly apply rewriting rules to transform symbols into other symbols. The objective is to start with a nonterminal symbol <code class="language-plaintext highlighter-rouge">S</code> (representing a sentence) and repeatedly apply context-free grammar rules until we generate a complete sentence of terminal symbols (i.e., words). The rule <code class="language-plaintext highlighter-rouge">S -&gt; N V</code>, for example, means that the <code class="language-plaintext highlighter-rouge">S</code> symbol can be rewritten as <code class="language-plaintext highlighter-rouge">N V</code> (a noun followed by a verb). If we also have the rule <code class="language-plaintext highlighter-rouge">N -&gt; "Holmes"</code> and the rule <code class="language-plaintext highlighter-rouge">V -&gt; "sat"</code>, we can generate the complete sentence <code class="language-plaintext highlighter-rouge">"Holmes sat."</code>.</p>

<p>Of course, noun phrases might not always be as simple as a single word like <code class="language-plaintext highlighter-rouge">"Holmes"</code>. We might have noun phrases like <code class="language-plaintext highlighter-rouge">"my companion"</code> or <code class="language-plaintext highlighter-rouge">"a country walk"</code> or <code class="language-plaintext highlighter-rouge">"the day before Thursday"</code>, which require more complex rules to account for. To account for the phrase <code class="language-plaintext highlighter-rouge">"my companion"</code>, for example, we might imagine a rule like:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>NP -&gt; N | Det N
</code></pre></div></div>

<p>In this rule, we say that an <code class="language-plaintext highlighter-rouge">NP</code> (a “noun phrase”) could be either just a noun (<code class="language-plaintext highlighter-rouge">N</code>) or a determiner (<code class="language-plaintext highlighter-rouge">Det</code>) followed by a noun, where determiners include words like <code class="language-plaintext highlighter-rouge">"a"</code>, <code class="language-plaintext highlighter-rouge">"the"</code>, and <code class="language-plaintext highlighter-rouge">"my"</code>. The vertical bar (<code class="language-plaintext highlighter-rouge">|</code>) just indicates that there are multiple possible ways to rewrite an <code class="language-plaintext highlighter-rouge">NP</code>, with each possible rewrite separated by a bar.</p>

<p>To incorporate this rule into how we parse a sentence (<code class="language-plaintext highlighter-rouge">S</code>), we’ll also need to modify our <code class="language-plaintext highlighter-rouge">S -&gt; N V</code> rule to allow for noun phrases (<code class="language-plaintext highlighter-rouge">NP</code>s) as the subject of our sentence. See how? And to account for more complex types of noun phrases, we may need to modify our grammar even further.</p>


<h2 id="understanding">Understanding</h2>

<p>First, look at the text files in the <code class="language-plaintext highlighter-rouge">sentences</code> directory. Each file contains an English sentence. Your goal in this problem is to write a parser that is able to parse all of these sentences.</p>

<p>Take a look now at <code class="language-plaintext highlighter-rouge">parser.py</code>, and notice the context free grammar rules defined at the top of the file. We’ve already defined for you a set of rules for generating terminal symbols (in the global variable <code class="language-plaintext highlighter-rouge">TERMINALS</code>). Notice that <code class="language-plaintext highlighter-rouge">Adj</code> is a nonterminal symbol that generates adjectives, <code class="language-plaintext highlighter-rouge">Adv</code> generates adverbs, <code class="language-plaintext highlighter-rouge">Conj</code> generates conjunctions, <code class="language-plaintext highlighter-rouge">Det</code> generates determiners, <code class="language-plaintext highlighter-rouge">N</code> generates nouns (spread across multiple lines for readability), <code class="language-plaintext highlighter-rouge">P</code> generates prepositions, and <code class="language-plaintext highlighter-rouge">V</code> generates verbs.</p>

<p>Next is the definition of <code class="language-plaintext highlighter-rouge">NONTERMINALS</code>, which will contain all of the context-free grammar rules for generating nonterminal symbols. Right now, there’s just a single rule: <code class="language-plaintext highlighter-rouge">S -&gt; N V</code>. With just that rule, we can generate sentences like <code class="language-plaintext highlighter-rouge">"Holmes arrived."</code> or <code class="language-plaintext highlighter-rouge">"He chuckled."</code>, but not sentences more complex than that. Editing the <code class="language-plaintext highlighter-rouge">NONTERMINALS</code> rules so that all of the sentences can be parsed will be up to you!</p>

<p>Next, take a look at the <code class="language-plaintext highlighter-rouge">main</code> function. It first accepts a sentence as input, either from a file or via user input. The sentence is preprocessed (via the <code class="language-plaintext highlighter-rouge">preprocess</code> function) and then parsed according to the context-free grammar defined by the file. The resulting trees are printed out, and all of the “noun phrase chunks” (defined in the Specification) are printed as well (via the <code class="language-plaintext highlighter-rouge">np_chunk</code> function).</p>

<p>In addition to writing context-free grammar rules for parsing these sentences, the <code class="language-plaintext highlighter-rouge">preprocess</code> and <code class="language-plaintext highlighter-rouge">np_chunk</code> functions are left up to you!</p>

<h2 id="specification">Specification</h2>

<div class="alert" data-alert="warning" role="alert"><p>An automated tool assists the staff in enforcing the constraints in the below specification. Your submission will fail if any of these are not handled properly, if you import modules other than those explicitly allowed, or if you modify functions other than as permitted.</p></div>

<p>Complete the implementation of <code class="language-plaintext highlighter-rouge">preprocess</code> and <code class="language-plaintext highlighter-rouge">np_chunk</code>, and complete the context-free grammar rules defined in <code class="language-plaintext highlighter-rouge">NONTERMINALS</code>.</p>

<ul>
  <li data-marker="*">The <code class="language-plaintext highlighter-rouge">preprocess</code> function should accept a <code class="language-plaintext highlighter-rouge">sentence</code> as input and return a lowercased list of its words.
    <ul>
      <li data-marker="*">You may assume that <code class="language-plaintext highlighter-rouge">sentence</code> will be a string.</li>
      <li data-marker="*">You should use <code class="language-plaintext highlighter-rouge">nltk</code>’s <a href="https://www.nltk.org/api/nltk.tokenize.html#nltk.tokenize.punkt.PunktLanguageVars.word_tokenize"><code class="language-plaintext highlighter-rouge">word_tokenize</code></a> function to perform tokenization.</li>
      <li data-marker="*">Your function should return a list of words, where each word is a lowercased string.</li>
      <li data-marker="*">Any word that doesn’t contain at least one alphabetic character (e.g. <code class="language-plaintext highlighter-rouge">.</code> or <code class="language-plaintext highlighter-rouge">28</code>) should be excluded from the returned list.</li>
    </ul>
  </li>
  <li data-marker="*">The <code class="language-plaintext highlighter-rouge">NONTERMINALS</code> global variable should be replaced with a set of context-free grammar rules that, when combined with the rules in <code class="language-plaintext highlighter-rouge">TERMINALS</code>, allow the parsing of all sentences in the <code class="language-plaintext highlighter-rouge">sentences/</code> directory.
    <ul>
      <li data-marker="*">Each rules must be on its own line. Each rule must include the <code class="language-plaintext highlighter-rouge">-&gt;</code> characters to denote which symbol is being replaced, and may optionally include <code class="language-plaintext highlighter-rouge">|</code> symbols if there are multiple ways to rewrite a symbol.</li>
      <li data-marker="*">You do not need to keep the existing rule <code class="language-plaintext highlighter-rouge">S -&gt; N V</code> in your solution, but your first rule must begin with <code class="language-plaintext highlighter-rouge">S -&gt;</code> since <code class="language-plaintext highlighter-rouge">S</code> (representing a sentence) is the starting symbol.</li>
      <li data-marker="*">You may add as many nonterminal symbols as you would like.</li>
      <li data-marker="*">Use the nonterminal symbol <code class="language-plaintext highlighter-rouge">NP</code> to represent a “noun phrase”, such as the subject of a sentence.</li>
    </ul>
  </li>
  <li data-marker="*">The <code class="language-plaintext highlighter-rouge">np_chunk</code> function should accept a <code class="language-plaintext highlighter-rouge">tree</code> representing the syntax of a sentence, and return a list of all of the noun phrase chunks in that sentence.
    <ul>
      <li data-marker="*">For this problem, a “noun phrase chunk” is defined as a noun phrase that doesn’t contain other noun phrases within it. Put more formally, a noun phrase chunk is a subtree of the original tree whose label is <code class="language-plaintext highlighter-rouge">NP</code> and that does not itself contain other noun phrases as subtrees.
        <ul>
          <li data-marker="*">For example, if <code class="language-plaintext highlighter-rouge">"the home"</code> is a noun phrase chunk, then <code class="language-plaintext highlighter-rouge">"the armchair in the home"</code> is not a noun phrase chunk, because the latter contains the former as a subtree.</li>
        </ul>
      </li>
      <li data-marker="*">You may assume that the input will be a <code class="language-plaintext highlighter-rouge">nltk.tree</code> object whose label is <code class="language-plaintext highlighter-rouge">S</code> (that is to say, the input will be a tree representing a sentence).</li>
      <li data-marker="*">Your function should return a list of <code class="language-plaintext highlighter-rouge">nltk.tree</code> objects, where each element has the label <code class="language-plaintext highlighter-rouge">NP</code>.</li>
      <li data-marker="*">You will likely find the documentation for <a href="https://www.nltk.org/_modules/nltk/tree.html"><code class="language-plaintext highlighter-rouge">nltk.tree</code></a> helpful for identifying how to manipulate a <code class="language-plaintext highlighter-rouge">nltk.tree</code> object.</li>
    </ul>
  </li>
</ul>

<p>You should not modify anything else in <code class="language-plaintext highlighter-rouge">parser.py</code> other than the functions the specification calls for you to implement, though you may write additional functions and/or import other Python standard library modules. You will need to modify the definition of <code class="language-plaintext highlighter-rouge">NONTERMINALS</code>, but you should not modify the definition of <code class="language-plaintext highlighter-rouge">TERMINALS</code>.</p>

<h2 id="hints">Hints</h2>

<ul>
  <li data-marker="*">It’s to be expected that your parser may generate some sentences that you believe are not syntactically or semantically well-formed. You need not worry, therefore, if your parser allows for parsing meaningless sentences like <code class="language-plaintext highlighter-rouge">"His Thursday chuckled in a paint."</code>
    <ul>
      <li data-marker="*">That said, you should avoid over-generation of sentences where possible. For example, your parser should definitely not accept sentences like <code class="language-plaintext highlighter-rouge">"Armchair on the sat Holmes."</code></li>
      <li data-marker="*">You should also avoid under-generation of sentences. A rule like <code class="language-plaintext highlighter-rouge">S -&gt; N V Det Adj Adj Adj N P Det N P Det N</code> would technically successfully generate sentence 10, but not in a way that is particularly useful or generalizable.</li>
      <li data-marker="*">The rules in the lecture source code are (intentionally) a very simplified rule set, and as a result may suffer from over-generation. You can (and should) make modifications to those rules to try to be as general as possible without over-generating. In particular, consider how you might get your parser to accept the sentence “Holmes sat in the armchair.” (and “Holmes sat in the red armchair.” and “Holmes sat in the little red armchair.”), but have it <em>not</em> accept the sentence “Holmes sat in the the armchair.”</li>
    </ul>
  </li>
  <li data-marker="*">It’s to be expected that your parser may generate multiple ways to parse a sentence. English grammar is inherently ambiguous!</li>
  <li data-marker="*">Within the <a href="https://www.nltk.org/_modules/nltk/tree.html"><code class="language-plaintext highlighter-rouge">nltk.tree</code></a> documentation, you may find the <code class="language-plaintext highlighter-rouge">label</code> and <code class="language-plaintext highlighter-rouge">subtrees</code> functions particularly useful.</li>
  <li data-marker="*">To focus on testing your parser before working on noun phrase chunking, it may be helpful to temporarily have <code class="language-plaintext highlighter-rouge">np_chunk</code> simply return an empty list <code class="language-plaintext highlighter-rouge">[]</code>, so that your program can operate without noun phrase chunking while you test the other parts of your program.</li>
</ul>

