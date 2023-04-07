# Questions

<p>Write an AI to answer questions.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$ python questions.py corpus
Query: What are the types of supervised learning?
Types of supervised learning algorithms include Active learning , classification and regression.

$ python questions.py corpus
Query: When was Python 3.0 released?
Python 3.0 was released on 3 December 2008.

$ python questions.py corpus
Query: How do neurons connect in a neural network?
Neurons of one layer connect only to neurons of the immediately preceding and immediately following layers.
</code></pre></div></div>



<h2 id="background">Background</h2>

<p>Question Answering (QA) is a field within natural language processing focused on designing systems that can answer questions. Among the more famous question answering systems is <a href="https://en.wikipedia.org/wiki/Watson_(computer)">Watson</a>, the IBM computer that competed (and won) on <em>Jeopardy!</em>. A question answering system of Watson’s accuracy requires enormous complexity and vast amounts of data, but in this problem, we’ll design a very simple question answering system based on inverse document frequency.</p>

<p>Our question answering system will perform two tasks: document retrieval and passage retrieval. Our system will have access to a corpus of text documents. When presented with a query (a question in English asked by the user), document retrieval will first identify which document(s) are most relevant to the query. Once the top documents are found, the top document(s) will be subdivided into passages (in this case, sentences) so that the most relevant passage to the question can be determined.</p>

<p>How do we find the most relevant documents and passages? To find the most relevant documents, we’ll use tf-idf to rank documents based both on term frequency for words in the query as well as inverse document frequency for words in the query. Once we’ve found the most relevant documents, there <a href="https://groups.csail.mit.edu/infolab/publications/Tellex-etal-SIGIR03.pdf">many possible metrics</a> for scoring passages, but we’ll use a combination of inverse document frequency and a query term density measure (described in the Specification).</p>

<p>More sophisticated question answering systems might employ other strategies (analyzing the type of question word used, looking for synonyms of query words, <a href="https://en.wikipedia.org/wiki/Lemmatisation">lemmatizing</a> to handle different forms of the same word, etc.) but we’ll leave those sorts of improvements as exercises for you to work on if you’d like to after you’ve completed this project!</p>



<h2 id="understanding">Understanding</h2>

<p>First, take a look at the documents in <code class="language-plaintext highlighter-rouge">corpus</code>. Each is a text file containing the contents of a Wikipedia page. Our goal is to write an AI that can find sentences from these files that are relevant to a user’s query. You are welcome and encouraged to add, remove, or modify files in the corpus if you’d like to experiment with answering queries based on a different corpus of documents. Just be sure each file in the corpus is a text file ending in <code class="language-plaintext highlighter-rouge">.txt</code>.</p>

<p>Now, take a look at <code class="language-plaintext highlighter-rouge">questions.py</code>. The global variable <code class="language-plaintext highlighter-rouge">FILE_MATCHES</code> specifies how many files should be matched for any given query. The global variable <code class="language-plaintext highlighter-rouge">SENTENCES_MATCHES</code> specifies how many sentences within those files should be matched for any given query. By default, each of these values is 1: our AI will find the top sentence from the top matching document as the answer to our question. You are welcome and encouraged to experiment with changing these values.</p>

<p>In the <code class="language-plaintext highlighter-rouge">main</code> function, we first load the files from the corpus directory into memory (via the <code class="language-plaintext highlighter-rouge">load_files</code> function). Each of the files is then tokenized (via <code class="language-plaintext highlighter-rouge">tokenize</code>) into a list of words, which then allows us to compute inverse document frequency values for each of the words (via <code class="language-plaintext highlighter-rouge">compute_idfs</code>). The user is then prompted to enter a query. The <code class="language-plaintext highlighter-rouge">top_files</code> function identifies the files that are the best match for the query. From those files, sentences are extracted, and the <code class="language-plaintext highlighter-rouge">top_sentences</code> function identifies the sentences that are the best match for the query.</p>

<p>The <code class="language-plaintext highlighter-rouge">load_files</code>, <code class="language-plaintext highlighter-rouge">tokenize</code>, <code class="language-plaintext highlighter-rouge">compute_idfs</code>, <code class="language-plaintext highlighter-rouge">top_files</code>, and <code class="language-plaintext highlighter-rouge">top_sentences</code> functions are left to you!</p>

<h2 id="specification">Specification</h2>

<div class="alert" data-alert="warning" role="alert"><p>An automated tool assists the staff in enforcing the constraints in the below specification. Your submission will fail if any of these are not handled properly, if you import modules other than those explicitly allowed, or if you modify functions other than as permitted.</p></div>

<p>Complete the implementation of <code class="language-plaintext highlighter-rouge">load_files</code>, <code class="language-plaintext highlighter-rouge">tokenize</code>, <code class="language-plaintext highlighter-rouge">compute_idfs</code>, <code class="language-plaintext highlighter-rouge">top_files</code>, and <code class="language-plaintext highlighter-rouge">top_sentences</code> in <code class="language-plaintext highlighter-rouge">questions.py</code>.</p>

<ul>
  <li data-marker="*">The <code class="language-plaintext highlighter-rouge">load_files</code> function should accept the name of a <code class="language-plaintext highlighter-rouge">directory</code> and return a dictionary mapping the filename of each <code class="language-plaintext highlighter-rouge">.txt</code> file inside that directory to the file’s contents as a string.
    <ul>
      <li data-marker="*">Your function should be platform-independent: that is to say, it should work regardless of operating system. Note that on macOS, the <code class="language-plaintext highlighter-rouge">/</code> character is used to separate path components, while the <code class="language-plaintext highlighter-rouge">\</code> character is used on Windows. Use <a href="https://docs.python.org/3/library/os.html"><code class="language-plaintext highlighter-rouge">os.sep</code></a> and <a href="https://docs.python.org/3/library/os.path.html#os.path.join"><code class="language-plaintext highlighter-rouge">os.path.join</code></a> as needed instead of using your platform’s specific separator character.</li>
      <li data-marker="*">In the returned dictionary, there should be one key named for each <code class="language-plaintext highlighter-rouge">.txt</code> file in the directory. The value associated with that key should be a string (the result of <code class="language-plaintext highlighter-rouge">read</code>ing the corresonding file).</li>
      <li data-marker="*">Each key should be just the filename, without including the directory name. For example, if the directory is called <code class="language-plaintext highlighter-rouge">corpus</code> and contains files <code class="language-plaintext highlighter-rouge">a.txt</code> and <code class="language-plaintext highlighter-rouge">b.txt</code>, the keys should be <code class="language-plaintext highlighter-rouge">a.txt</code> and <code class="language-plaintext highlighter-rouge">b.txt</code> and not <code class="language-plaintext highlighter-rouge">corpus/a.txt</code> and <code class="language-plaintext highlighter-rouge">corpus/b.txt</code>.</li>
    </ul>
  </li>
  <li data-marker="*">The <code class="language-plaintext highlighter-rouge">tokenize</code> function should accept a <code class="language-plaintext highlighter-rouge">document</code> (a string) as input, and return a list of all of the words in that document, in order and lowercased.
    <ul>
      <li data-marker="*">You should use <code class="language-plaintext highlighter-rouge">nltk</code>’s <a href="https://www.nltk.org/api/nltk.tokenize.html#nltk.tokenize.punkt.PunktLanguageVars.word_tokenize"><code class="language-plaintext highlighter-rouge">word_tokenize</code></a> function to perform tokenization.</li>
      <li data-marker="*">All words in the returned list should be lowercased.</li>
      <li data-marker="*">Filter out punctuation and stopwords (common words that are unlikely to be useful for querying). Punctuation is defined as any character in <code class="language-plaintext highlighter-rouge">string.punctuation</code> (after you <code class="language-plaintext highlighter-rouge">import string</code>). Stopwords are defined as any word in <code class="language-plaintext highlighter-rouge">nltk.corpus.stopwords.words("english")</code>.</li>
      <li data-marker="*">If a word appears multiple times in the <code class="language-plaintext highlighter-rouge">document</code>, it should also appear multiple times in the returned list (unless it was filtered out).</li>
    </ul>
  </li>
  <li data-marker="*">The <code class="language-plaintext highlighter-rouge">compute_idfs</code> function should accept a dictionary of <code class="language-plaintext highlighter-rouge">documents</code> and return a new dictionary mapping words to their IDF (inverse document frequency) values.
    <ul>
      <li data-marker="*">Assume that <code class="language-plaintext highlighter-rouge">documents</code> will be a dictionary mapping names of documents to a list of words in that document.</li>
      <li data-marker="*">The returned dictionary should map every word that appears in at least one of the documents to its inverse document frequency value.</li>
      <li data-marker="*">Recall that the inverse document frequency of a word is defined by taking the natural logarithm of the number of documents divided by the number of documents in which the word appears.</li>
    </ul>
  </li>
  <li data-marker="*">The <code class="language-plaintext highlighter-rouge">top_files</code> function should, given a <code class="language-plaintext highlighter-rouge">query</code> (a set of words), <code class="language-plaintext highlighter-rouge">files</code> (a dictionary mapping names of files to a list of their words), and <code class="language-plaintext highlighter-rouge">idfs</code> (a dictionary mapping words to their IDF values), return a list of the filenames of the the <code class="language-plaintext highlighter-rouge">n</code> top files that match the query, ranked according to tf-idf.
    <ul>
      <li data-marker="*">The returned list of filenames should be of length <code class="language-plaintext highlighter-rouge">n</code> and should be ordered with the best match first.</li>
      <li data-marker="*">Files should be ranked according to the sum of tf-idf values for any word in the query that also appears in the file. Words in the query that do not appear in the file should not contribute to the file’s score.</li>
      <li data-marker="*">Recall that tf-idf for a term is computed by multiplying the number of times the term appears in the document by the IDF value for that term.</li>
      <li data-marker="*">You may assume that <code class="language-plaintext highlighter-rouge">n</code> will not be greater than the total number of files.</li>
    </ul>
  </li>
  <li data-marker="*">The <code class="language-plaintext highlighter-rouge">top_sentences</code> function should, given a <code class="language-plaintext highlighter-rouge">query</code> (a set of words), <code class="language-plaintext highlighter-rouge">sentences</code> (a dictionary mapping sentences to a list of their words), and <code class="language-plaintext highlighter-rouge">idfs</code> (a dictionary mapping words to their IDF values), return a list of the <code class="language-plaintext highlighter-rouge">n</code> top sentences that match the query, ranked according to IDF.
    <ul>
      <li data-marker="*">The returned list of sentences should be of length <code class="language-plaintext highlighter-rouge">n</code> and should be ordered with the best match first.</li>
      <li data-marker="*">Sentences should be ranked according to “matching word measure”: namely, the sum of IDF values for any word in the query that also appears in the sentence. Note that term frequency should not be taken into account here, only inverse document frequency.</li>
      <li data-marker="*">If two sentences have the same value according to the matching word measure, then sentences with a higher “query term density” should be preferred. Query term density is defined as the proportion of words in the sentence that are also words in the query. For example, if a sentence has 10 words, 3 of which are in the query, then the sentence’s query term density is <code class="language-plaintext highlighter-rouge">0.3</code>.</li>
      <li data-marker="*">You may assume that <code class="language-plaintext highlighter-rouge">n</code> will not be greater than the total number of sentences.</li>
    </ul>
  </li>
</ul>

<p>You should not modify anything else in <code class="language-plaintext highlighter-rouge">questions.py</code> other than the functions the specification calls for you to implement, though you may write additional functions, add new global constant variables, and/or import other Python standard library modules.</p>

