# PageRank

<p>Write an AI to rank web pages by importance.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$ python pagerank.py corpus0
PageRank Results from Sampling (n = 10000)
  1.html: 0.2223
  2.html: 0.4303
  3.html: 0.2145
  4.html: 0.1329
PageRank Results from Iteration
  1.html: 0.2202
  2.html: 0.4289
  3.html: 0.2202
  4.html: 0.1307
</code></pre></div></div>


<h2 id="background">Background</h2>

<p>When search engines like Google display search results, they do so by placing more “important” and higher-quality pages higher in the search results than less important pages. But how does the search engine know which pages are more important than other pages?</p>

<p>One heuristic might be that an “important” page is one that many other pages link to, since it’s reasonable to imagine that more sites will link to a higher-quality webpage than a lower-quality webpage. We could therefore imagine a system where each page is given a rank according to the number of incoming links it has from other pages, and higher ranks would signal higher importance.</p>

<p>But this definition isn’t perfect: if someone wants to make their page seem more important, then under this system, they could simply create many other pages that link to their desired page to artificially inflate its rank.</p>

<p>For that reason, the PageRank algorithm was created by Google’s co-founders (including Larry Page, for whom the algorithm was named). In PageRank’s algorithm, a website is more important if it is linked to by other important websites, and links from less important websites have their links weighted less. This definition seems a bit circular, but it turns out that there are multiple strategies for calculating these rankings.</p>

<h3 id="random-surfer-model">Random Surfer Model</h3>

<p>One way to think about PageRank is with the random surfer model, which considers the behavior of a hypothetical surfer on the internet who clicks on links at random. Consider the corpus of web pages below, where an arrow between two pages indicates a link from one page to another.</p>

<p><img src="images/corpus.png" alt="Corpus of web pages"></p>

<p>The random surfer model imagines a surfer who starts with a web page at random, and then randomly chooses links to follow. If the surfer is on Page 2, for example, they would randomly choose between Page 1 and Page 3 to visit next (duplicate links on the same page are treated as a single link, and links from a page to itself are ignored as well). If they chose Page 3, the surfer would then randomly choose between Page 2 and Page 4 to visit next.</p>

<p>A page’s PageRank, then, can be described as the probability that a random surfer is on that page at any given time. After all, if there are more links to a particular page, then it’s more likely that a random surfer will end up on that page. Moreover, a link from a more important site is more likely to be clicked on than a link from a less important site that fewer pages link to, so this model handles weighting links by their importance as well.</p>

<p>One way to interpret this model is as a Markov Chain, where each page represents a state, and each page has a transition model that chooses among its links at random. At each time step, the state switches to one of the pages linked to by the current state.</p>

<p>By sampling states randomly from the Markov Chain, we can get an estimate for each page’s PageRank. We can start by choosing a page at random, then keep following links at random, keeping track of how many times we’ve visited each page. After we’ve gathered all of our samples (based on a number we choose in advance), the proportion of the time we were on each page might be an estimate for that page’s rank.</p>

<p>However, this definition of PageRank proves slightly problematic, if we consider a network of pages like the below.</p>

<p><img src="images/network_disconnected.png" alt="Disconnected corpus of web pages"></p>

<p>Imagine we randomly started by sampling Page 5. We’d then have no choice but to go to Page 6, and then no choice but to go to Page 5 after that, and then Page 6 again, and so forth. We’d end up with an estimate of 0.5 for the PageRank for Pages 5 and 6, and an estimate of 0 for the PageRank of all the remaining pages, since we spent all our time on Pages 5 and 6 and never visited any of the other pages.</p>

<p>To ensure we can always get to somewhere else in the corpus of web pages, we’ll introduce to our model a damping factor <code class="language-plaintext highlighter-rouge">d</code>. With probability <code class="language-plaintext highlighter-rouge">d</code> (where <code class="language-plaintext highlighter-rouge">d</code> is usually set around <code class="language-plaintext highlighter-rouge">0.85</code>), the random surfer will choose from one of the links on the current page at random. But otherwise (with probability <code class="language-plaintext highlighter-rouge">1 - d</code>), the random surfer chooses one out of all of the pages in the corpus at random (including the one they are currently on).</p>

<p>Our random surfer now starts by choosing a page at random, and then, for each additional sample we’d like to generate, chooses a link from the current page at random with probability <code class="language-plaintext highlighter-rouge">d</code>, and chooses any page at random with probability <code class="language-plaintext highlighter-rouge">1 - d</code>. If we keep track of how many times each page has shown up as a sample, we can treat the proportion of states that were on a given page as its PageRank.</p>

<h3 id="iterative-algorithm">Iterative Algorithm</h3>

<p>We can also define a page’s PageRank using a recursive mathematical expression. Let <code class="language-plaintext highlighter-rouge">PR(p)</code> be the PageRank of a given page <code class="language-plaintext highlighter-rouge">p</code>: the probability that a random surfer ends up on that page. How do we define <code class="language-plaintext highlighter-rouge">PR(p)</code>? Well, we know there are two ways that a random surfer could end up on the page:</p>

<ol>
  <li>With probability <code class="language-plaintext highlighter-rouge">1 - d</code>, the surfer chose a page at random and ended up on page <code class="language-plaintext highlighter-rouge">p</code>.</li>
  <li>With probability <code class="language-plaintext highlighter-rouge">d</code>, the surfer followed a link from a page <code class="language-plaintext highlighter-rouge">i</code> to page <code class="language-plaintext highlighter-rouge">p</code>.</li>
</ol>

<p>The first condition is fairly straightforward to express mathematically: it’s <code class="language-plaintext highlighter-rouge">1 - d</code> divided by <code class="language-plaintext highlighter-rouge">N</code>, where <code class="language-plaintext highlighter-rouge">N</code> is the total number of pages across the entire corpus. This is because the <code class="language-plaintext highlighter-rouge">1 - d</code> probability of choosing a page at random is split evenly among all <code class="language-plaintext highlighter-rouge">N</code> possible pages.</p>

<p>For the second condition, we need to consider each possible page <code class="language-plaintext highlighter-rouge">i</code> that links to page <code class="language-plaintext highlighter-rouge">p</code>. For each of those incoming pages, let <code class="language-plaintext highlighter-rouge">NumLinks(i)</code> be the number of links on page <code class="language-plaintext highlighter-rouge">i</code>. Each page <code class="language-plaintext highlighter-rouge">i</code> that links to <code class="language-plaintext highlighter-rouge">p</code> has its own PageRank, <code class="language-plaintext highlighter-rouge">PR(i)</code>, representing the probability that we are on page <code class="language-plaintext highlighter-rouge">i</code> at any given time. And since from page <code class="language-plaintext highlighter-rouge">i</code> we travel to any of that page’s links with equal probability, we divide <code class="language-plaintext highlighter-rouge">PR(i)</code> by the number of links <code class="language-plaintext highlighter-rouge">NumLinks(i)</code> to get the probability that we were on page <code class="language-plaintext highlighter-rouge">i</code> and chose the link to page <code class="language-plaintext highlighter-rouge">p</code>.</p>

<p>This gives us the following definition for the PageRank for a page <code class="language-plaintext highlighter-rouge">p</code>.</p>

$$PR\left ( p \right )= \frac{1-d}{N} + d*\sum \frac{PR_{i}}{NumLinks_{i}}$$

<p>In this formula, <code class="language-plaintext highlighter-rouge">d</code> is the damping factor, <code class="language-plaintext highlighter-rouge">N</code> is the total number of pages in the corpus, <code class="language-plaintext highlighter-rouge">i</code> ranges over all pages that link to page <code class="language-plaintext highlighter-rouge">p</code>, and <code class="language-plaintext highlighter-rouge">NumLinks(i)</code> is the number of links present on page <code class="language-plaintext highlighter-rouge">i</code>.</p>

<p>How would we go about calculating PageRank values for each page, then? We can do so via iteration: start by assuming the PageRank of every page is <code class="language-plaintext highlighter-rouge">1 / N</code> (i.e., equally likely to be on any page). Then, use the above formula to calculate new PageRank values for each page, based on the previous PageRank values. If we keep repeating this process, calculating a new set of PageRank values for each page based on the previous set of PageRank values, eventually the PageRank values will converge (i.e., not change by more than a small threshold with each iteration).</p>

<p>In this project, you’ll implement both such approaches for calculating PageRank – calculating both by sampling pages from a Markov Chain random surfer and by iteratively applying the PageRank formula.</p>



<h2 id="understanding">Understanding</h2>

<p>Open up <code class="language-plaintext highlighter-rouge">pagerank.py</code>. Notice first the definition of two constants at the top of the file: <code class="language-plaintext highlighter-rouge">DAMPING</code> represents the damping factor and is initially set to <code class="language-plaintext highlighter-rouge">0.85</code>. <code class="language-plaintext highlighter-rouge">SAMPLES</code> represents the number of samples we’ll use to estimate PageRank using the sampling method, initially set to 10,000 samples.</p>

<p>Now, take a look at the <code class="language-plaintext highlighter-rouge">main</code> function. It expects a command-line argument, which will be the name of a directory of a corpus of web pages we’d like to compute PageRanks for. The <code class="language-plaintext highlighter-rouge">crawl</code> function takes that directory, parses all of the HTML files in the directory, and returns a dictionary representing the corpus. The keys in that dictionary represent pages (e.g., <code class="language-plaintext highlighter-rouge">"2.html"</code>), and the values of the dictionary are a set of all of the pages linked to by the key (e.g. <code class="language-plaintext highlighter-rouge">{"1.html", "3.html"}</code>).</p>

<p>The <code class="language-plaintext highlighter-rouge">main</code> function then calls the <code class="language-plaintext highlighter-rouge">sample_pagerank</code> function, whose purpose is to estimate the PageRank of each page by sampling. The function takes as arguments the corpus of pages generated by <code class="language-plaintext highlighter-rouge">crawl</code>, as well as the damping factor and number of samples to use. Ultimately, <code class="language-plaintext highlighter-rouge">sample_pagerank</code> should return a dictionary where the keys are each page name and the values are each page’s estimated PageRank (a number between 0 and 1).</p>

<p>The <code class="language-plaintext highlighter-rouge">main</code> function also calls the <code class="language-plaintext highlighter-rouge">iterate_pagerank</code> function, which will also calculate PageRank for each page, but using the iterative formula method instead of by sampling. The return value is expected to be in the same format, and we would hope that the output of these two functions should be similar when given the same corpus!</p>

<h2 id="specification">Specification</h2>

<div class="alert" data-alert="warning" role="alert"><p>An automated tool assists the staff in enforcing the constraints in the below specification. Your submission will fail if any of these are not handled properly, if you import modules other than those explicitly allowed, or if you modify functions other than as permitted.</p></div>

<div class="alert" data-alert="primary" role="alert"><p>Many students have had issues with the autograders on this assignment because of how their dictionaries are constructed (that is to say, <em>improperly</em>). It is imperative that you read this specification carefully and implement its requirements exactly. As noted above, humans are not going to overrule the results of the autograder, so please do not ask them to. You may get away with running things locally and everything seems fine, but that’s because the program doesn’t care how your dictionaries are constructed. The autograder does!</p></div>

<p>Complete the implementation of <code class="language-plaintext highlighter-rouge">transition_model</code>, <code class="language-plaintext highlighter-rouge">sample_pagerank</code>, and <code class="language-plaintext highlighter-rouge">iterate_pagerank</code>.</p>

<p>The <code class="language-plaintext highlighter-rouge">transition_model</code> should return a dictionary representing the probability distribution over which page a random surfer would visit next, given a corpus of pages, a current page, and a damping factor.</p>

<ul>
  <li data-marker="*">The function accepts three arguments: <code class="language-plaintext highlighter-rouge">corpus</code>, <code class="language-plaintext highlighter-rouge">page</code>, and <code class="language-plaintext highlighter-rouge">damping_factor</code>.
    <ul>
      <li data-marker="*">The <code class="language-plaintext highlighter-rouge">corpus</code> is a Python dictionary mapping a page name to a set of all pages linked to by that page.</li>
      <li data-marker="*">The <code class="language-plaintext highlighter-rouge">page</code> is a string representing which page the random surfer is currently on.</li>
      <li data-marker="*">The <code class="language-plaintext highlighter-rouge">damping_factor</code> is a floating point number representing the damping factor to be used when generating the probabilities.</li>
    </ul>
  </li>
  <li data-marker="*">The return value of the function should be a Python dictionary with one key for each page in the corpus. Each key should be mapped to a value representing the probability that a random surfer would choose that page next. The values in this returned probability distribution should sum to <code class="language-plaintext highlighter-rouge">1</code>.
    <ul>
      <li data-marker="*">With probability <code class="language-plaintext highlighter-rouge">damping_factor</code>, the random surfer should randomly choose one of the links from <code class="language-plaintext highlighter-rouge">page</code> with equal probability.</li>
      <li data-marker="*">With probability <code class="language-plaintext highlighter-rouge">1 - damping_factor</code>, the random surfer should randomly choose one of all pages in the corpus with equal probability.</li>
    </ul>
  </li>
  <li data-marker="*">For example, if the <code class="language-plaintext highlighter-rouge">corpus</code> were <code class="language-plaintext highlighter-rouge">{"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}</code>, the <code class="language-plaintext highlighter-rouge">page</code> was <code class="language-plaintext highlighter-rouge">"1.html"</code>, and the <code class="language-plaintext highlighter-rouge">damping_factor</code> was <code class="language-plaintext highlighter-rouge">0.85</code>, then the output of <code class="language-plaintext highlighter-rouge">transition_model</code> should be <code class="language-plaintext highlighter-rouge">{"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}</code>. This is because with probability <code class="language-plaintext highlighter-rouge">0.85</code>, we choose randomly to go from page 1 to either page 2 or page 3 (so each of page 2 or page 3 has probability <code class="language-plaintext highlighter-rouge">0.425</code> to start), but every page gets an additional <code class="language-plaintext highlighter-rouge">0.05</code> because with probability <code class="language-plaintext highlighter-rouge">0.15</code> we choose randomly among all three of the pages.</li>
  <li data-marker="*">If <code class="language-plaintext highlighter-rouge">page</code> has no outgoing links, then <code class="language-plaintext highlighter-rouge">transition_model</code> should return a probability distribution that chooses randomly among all pages with equal probability. (In other words, if a page has no links, we can pretend it has links to all pages in the corpus, including itself.)</li>
</ul>

<p>The <code class="language-plaintext highlighter-rouge">sample_pagerank</code> function should accept a corpus of web pages, a damping factor, and a number of samples, and return an estimated PageRank for each page.</p>

<ul>
  <li data-marker="*">The function accepts three arguments: <code class="language-plaintext highlighter-rouge">corpus</code>, a <code class="language-plaintext highlighter-rouge">damping_factor</code>, and <code class="language-plaintext highlighter-rouge">n</code>.
    <ul>
      <li data-marker="*">The <code class="language-plaintext highlighter-rouge">corpus</code> is a Python dictionary mapping a page name to a set of all pages linked to by that page.</li>
      <li data-marker="*">The <code class="language-plaintext highlighter-rouge">damping_factor</code> is a floating point number representing the damping factor to be used by the transition model.</li>
      <li data-marker="*"><code class="language-plaintext highlighter-rouge">n</code> is an integer representing the number of samples that should be generated to estimate PageRank values.</li>
    </ul>
  </li>
  <li data-marker="*">The return value of the function should be a Python dictionary with one key for each page in the corpus. Each key should be mapped to a value representing that page’s estimated PageRank (i.e., the proportion of all the samples that corresponded to that page). The values in this dictionary should sum to <code class="language-plaintext highlighter-rouge">1</code>.</li>
  <li data-marker="*">The first sample should be generated by choosing from a page at random.</li>
  <li data-marker="*">For each of the remaining samples, the next sample should be generated from the previous sample based on the previous sample’s transition model.
    <ul>
      <li data-marker="*">You will likely want to pass the previous sample into your <code class="language-plaintext highlighter-rouge">transition_model</code> function, along with the <code class="language-plaintext highlighter-rouge">corpus</code> and the <code class="language-plaintext highlighter-rouge">damping_factor</code>, to get the probabilities for the next sample.</li>
      <li data-marker="*">For example, if the transition probabilities are <code class="language-plaintext highlighter-rouge">{"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}</code>, then 5% of the time the next sample generated should be <code class="language-plaintext highlighter-rouge">"1.html"</code>, 47.5% of the time the next sample generated should be <code class="language-plaintext highlighter-rouge">"2.html"</code>, and 47.5% of the time the next sample generated should be <code class="language-plaintext highlighter-rouge">"3.html"</code>.</li>
    </ul>
  </li>
  <li data-marker="*">You may assume that <code class="language-plaintext highlighter-rouge">n</code> will be at least <code class="language-plaintext highlighter-rouge">1</code>.</li>
</ul>

<p>The <code class="language-plaintext highlighter-rouge">iterate_pagerank</code> function should accept a corpus of web pages and a damping factor, calculate PageRanks based on the iteration formula described above, and return each page’s PageRank accurate to within <code class="language-plaintext highlighter-rouge">0.001</code>.</p>

<ul>
  <li data-marker="*">The function accepts two arguments: <code class="language-plaintext highlighter-rouge">corpus</code> and <code class="language-plaintext highlighter-rouge">damping_factor</code>.
    <ul>
      <li data-marker="*">The <code class="language-plaintext highlighter-rouge">corpus</code> is a Python dictionary mapping a page name to a set of all pages linked to by that page.</li>
      <li data-marker="*">The <code class="language-plaintext highlighter-rouge">damping_factor</code> is a floating point number representing the damping factor to be used in the PageRank formula.</li>
    </ul>
  </li>
  <li data-marker="*">The return value of the function should be a Python dictionary with one key for each page in the corpus. Each key should be mapped to a value representing that page’s PageRank. The values in this dictionary should sum to <code class="language-plaintext highlighter-rouge">1</code>.</li>
  <li data-marker="*">The function should begin by assigning each page a rank of <code class="language-plaintext highlighter-rouge">1 / N</code>, where <code class="language-plaintext highlighter-rouge">N</code> is the total number of pages in the corpus.</li>
  <li data-marker="*">The function should then repeatedly calculate new rank values based on all of the current rank values, according to the PageRank formula in the “Background” section. (i.e., calculating a page’s PageRank based on the PageRanks of all pages that link to it).
    <ul>
      <li data-marker="*">A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).</li>
    </ul>
  </li>
  <li data-marker="*">This process should repeat until no PageRank value changes by more than <code class="language-plaintext highlighter-rouge">0.001</code> between the current rank values and the new rank values.</li>
</ul>

<p>You should not modify anything else in <code class="language-plaintext highlighter-rouge">pagerank.py</code> other than the three functions the specification calls for you to implement, though you may write additional functions and/or import other Python standard library modules. You may also import <code class="language-plaintext highlighter-rouge">numpy</code> or <code class="language-plaintext highlighter-rouge">pandas</code>, if familiar with them, but you should not use any other third-party Python modules.</p>

<h2 id="hints">Hints</h2>

<ul>
  <li data-marker="*">You may find the functions in Python’s <a href="https://docs.python.org/3/library/random.html"><code class="language-plaintext highlighter-rouge">random</code></a> module helpful for making decisions pseudorandomly.</li>
</ul>

</html>