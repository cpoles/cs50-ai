# Heredity

<p>Write an AI to assess the likelihood that a person will have a particular genetic trait.</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$ python heredity.py data/family0.csv
Harry:
  Gene:
    2: 0.0092
    1: 0.4557
    0: 0.5351
  Trait:
    True: 0.2665
    False: 0.7335
James:
  Gene:
    2: 0.1976
    1: 0.5106
    0: 0.2918
  Trait:
    True: 1.0000
    False: 0.0000
Lily:
  Gene:
    2: 0.0036
    1: 0.0136
    0: 0.9827
  Trait:
    True: 0.0000
    False: 1.0000
</code></pre></div></div>

<h2 id="background">Background</h2>

<p>Mutated versions of the <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1285178/">GJB2 gene</a> are one of the leading causes of hearing impairment in newborns. Each person carries two versions of the gene, so each person has the potential to possess either 0, 1, or 2 copies of the hearing impairment version GJB2. Unless a person undergoes genetic testing, though, it’s not so easy to know how many copies of mutated GJB2 a person has. This is some “hidden state”: information that has an effect that we can observe (hearing impairment), but that we don’t necessarily directly know. After all, some people might have 1 or 2 copies of mutated GJB2 but not exhibit hearing impairment, while others might have no copies of mutated GJB2 yet still exhibit hearing impairment.</p>

<p>Every child inherits one copy of the GJB2 gene from each of their parents. If a parent has two copies of the mutated gene, then they will pass the mutated gene on to the child; if a parent has no copies of the mutated gene, then they will not pass the mutated gene on to the child; and if a parent has one copy of the mutated gene, then the gene is passed on to the child with probability 0.5. After a gene is passed on, though, it has some probability of undergoing additional mutation: changing from a version of the gene that causes hearing impairment to a version that doesn’t, or vice versa.</p>

<p>We can attempt to model all of these relationships by forming a Bayesian Network of all the relevant variables, as in the one below, which considers a family of two parents and a single child.</p>

![Screenshot](./images/BayesianNetwork.png)

<p>Each person in the family has a <code class="language-plaintext highlighter-rouge">Gene</code> random variable representing how many copies of a particular gene (e.g., the hearing impairment version of GJB2) a person has: a value that is 0, 1, or 2. Each person in the family also has a <code class="language-plaintext highlighter-rouge">Trait</code> random variable, which is <code class="language-plaintext highlighter-rouge">yes</code> or <code class="language-plaintext highlighter-rouge">no</code> depending on whether that person expresses a trait (e.g., hearing impairment) based on that gene. There’s an arrow from each person’s <code class="language-plaintext highlighter-rouge">Gene</code> variable to their <code class="language-plaintext highlighter-rouge">Trait</code> variable to encode the idea that a person’s genes affect the probability that they have a particular trait. Meanwhile, there’s also an arrow from both the mother and father’s <code class="language-plaintext highlighter-rouge">Gene</code> random variable to their child’s <code class="language-plaintext highlighter-rouge">Gene</code> random variable: the child’s genes are dependent on the genes of their parents.</p>

<p>Your task in this project is to use this model to make inferences about a population. Given information about people, who their parents are, and whether they have a particular observable trait (e.g. hearing loss) caused by a given gene, your AI will infer the probability distribution for each person’s genes, as well as the probability distribution for whether any person will exhibit the trait in question.</p>


<h2 id="understanding">Understanding</h2>

<p>Take a look at one of the sample data sets in the <code class="language-plaintext highlighter-rouge">data</code> directory by opening up <code class="language-plaintext highlighter-rouge">data/family0.csv</code> (you can open it up in a text editor, or in a spreadsheet application like Google Sheets, Excel, or Apple Numbers). Notice that the first row defines the columns for this CSV file: <code class="language-plaintext highlighter-rouge">name</code>, <code class="language-plaintext highlighter-rouge">mother</code>, <code class="language-plaintext highlighter-rouge">father</code>, and <code class="language-plaintext highlighter-rouge">trait</code>. The next row indicates that Harry has Lily as a mother, James as a father, and the empty cell for <code class="language-plaintext highlighter-rouge">trait</code> means we don’t know whether Harry has the trait or not. James, meanwhile, has no parents listed in the our data set (as indicated by the empty cells for <code class="language-plaintext highlighter-rouge">mother</code> and <code class="language-plaintext highlighter-rouge">father</code>), and does exhibit the trait (as indicated by the <code class="language-plaintext highlighter-rouge">1</code> in the <code class="language-plaintext highlighter-rouge">trait</code> cell). Lily, on the other hand, also has no parents listed in the data set, but does not exhibit the trait (as indicated by the <code class="language-plaintext highlighter-rouge">0</code> in the <code class="language-plaintext highlighter-rouge">trait</code> cell).</p>

<p>Open up <code class="language-plaintext highlighter-rouge">heredity.py</code> and take a look first at the definition of <code class="language-plaintext highlighter-rouge">PROBS</code>. <code class="language-plaintext highlighter-rouge">PROBS</code> is a dictionary containing a number of constants representing probabilities of various different events. All of these events have to do with how many copies of a particular gene a person has (hereafter referred to as simply “the gene”), and whether a person exhibits a particular trait (hereafter referred to as “the trait”) based on that gene. The data here is loosely based on the probabilities for the hearing impairment version of the GJB2 gene and the hearing impairment trait, but by changing these values, you could use your AI to draw inferences about other genes and traits as well!</p>

<p>First, <code class="language-plaintext highlighter-rouge">PROBS["gene"]</code> represents the unconditional probability distribution over the gene (i.e., the probability if we know nothing about that person’s parents). Based on the data in the distribution code, it would seem that in the population, there’s a 1% chance of having 2 copies of the gene, a 3% chance of having 1 copy of the gene, and a 96% chance of having 0 copies of the gene.</p>

<p>Next, <code class="language-plaintext highlighter-rouge">PROBS["trait"]</code> represents the conditional probability that a person exhibits a trait (like hearing impairment). This is actually three different probability distributions: one for each possible value for <code class="language-plaintext highlighter-rouge">gene</code>. So <code class="language-plaintext highlighter-rouge">PROBS["trait"][2]</code> is the probability distribution that a person has the trait given that they have two versions of the gene: in this case, they have a 65% chance of exhibiting the trait, and a 35% chance of not exhibiting the trait. Meanwhile, if a person has 0 copies of the gene, they have a 1% chance of exhibiting the trait, and a 99% chance of not exhibiting the trait.</p>

<p>Finally, <code class="language-plaintext highlighter-rouge">PROBS["mutation"]</code> is the probability that a gene mutates from being the gene in question to not being that gene, and vice versa. If a mother has two versions of the gene, for example, and therefore passes one on to her child, there’s a 1% chance it mutates into not being the target gene anymore. Conversely, if a mother has no versions of the gene, and therefore does not pass it onto her child, there’s a 1% chance it mutates into being the target gene. It’s therefore possible that even if neither parent has any copies of the gene in question, their child might have 1 or even 2 copies of the gene.</p>

<p>Ultimately, the probabilities you calculate will be based on these values in <code class="language-plaintext highlighter-rouge">PROBS</code>.</p>

<p>Now, take a look at the <code class="language-plaintext highlighter-rouge">main</code> function. The function first loads data from a file into a dictionary <code class="language-plaintext highlighter-rouge">people</code>. <code class="language-plaintext highlighter-rouge">people</code> maps each person’s name to another dictionary containing information about them: including their name, their mother (if one is listed in the data set), their father (if one is listed in the data set), and whether they are observed to have the trait in question (<code class="language-plaintext highlighter-rouge">True</code> if they do, <code class="language-plaintext highlighter-rouge">False</code> if they don’t, and <code class="language-plaintext highlighter-rouge">None</code> if we don’t know).</p>

<p>Next, <code class="language-plaintext highlighter-rouge">main</code> defines a dictionary of <code class="language-plaintext highlighter-rouge">probabilities</code>, with all probabilities initially set to 0. This is ultimately what your project will compute: for each person, your AI will calculate the probability distribution over how many of copies of the gene they have, as well as whether they have the trait or not. <code class="language-plaintext highlighter-rouge">probabilities["Harry"]["gene"][1]</code>, for example, will be the probability that Harry has 1 copy of the gene, and <code class="language-plaintext highlighter-rouge">probabilities["Lily"]["trait"][False]</code> will be the probability that Lily does not exhibit the trait.</p>

<p>If unfamiliar, this <code class="language-plaintext highlighter-rouge">probabilities</code> dictionary is created using a Python <a href="https://www.python.org/dev/peps/pep-0274/">dictionary comprehension</a>, which in this case creates one key/value pair for each <code class="language-plaintext highlighter-rouge">person</code> in our dictionary of <code class="language-plaintext highlighter-rouge">people</code>.</p>

<p>Ultimately, we’re looking to calculate these probabilities based on some evidence: given that we know certain people do or do not exhibit the trait, we’d like to determine these probabilities. Recall from lecture that we can calculate a conditional probability by summing up all of the joint probabilities that satisfy the evidence, and then normalize those probabilities so that they each sum to 1. Your task in this project is to implement three functions to do just that: <code class="language-plaintext highlighter-rouge">joint_probability</code> to compute a joint probability, <code class="language-plaintext highlighter-rouge">update</code> to add the newly computed joint probability to the existing probability distribution, and then <code class="language-plaintext highlighter-rouge">normalize</code> to ensure all probability distributions sum to 1 at the end.</p>

<h2 id="specification">Specification</h2>

<div class="alert" data-alert="warning" role="alert"><p>An automated tool assists the staff in enforcing the constraints in the below specification. Your submission will fail if any of these are not handled properly, if you import modules other than those explicitly allowed, or if you modify functions other than as permitted.</p></div>

<p>Complete the implementations of <code class="language-plaintext highlighter-rouge">joint_probability</code>, <code class="language-plaintext highlighter-rouge">update</code>, and <code class="language-plaintext highlighter-rouge">normalize</code>.</p>

<p>The <code class="language-plaintext highlighter-rouge">joint_probability</code> function should take as input a dictionary of people, along with data about who has how many copies of each of the genes, and who exhibits the trait. The function should return the joint probability of all of those events taking place.</p>

<ul>
  <li data-marker="*">The function accepts four values as input: <code class="language-plaintext highlighter-rouge">people</code>, <code class="language-plaintext highlighter-rouge">one_gene</code>, <code class="language-plaintext highlighter-rouge">two_genes</code>, and <code class="language-plaintext highlighter-rouge">have_trait</code>.
    <ul>
      <li data-marker="*"><code class="language-plaintext highlighter-rouge">people</code> is a dictionary of people as described in the “Understanding” section. The keys represent names, and the values are dictionaries that contain <code class="language-plaintext highlighter-rouge">mother</code> and <code class="language-plaintext highlighter-rouge">father</code> keys. You may assume that either <code class="language-plaintext highlighter-rouge">mother</code> and <code class="language-plaintext highlighter-rouge">father</code> are both blank (no parental information in the data set), or <code class="language-plaintext highlighter-rouge">mother</code> and <code class="language-plaintext highlighter-rouge">father</code> will both refer to other people in the <code class="language-plaintext highlighter-rouge">people</code> dictionary.</li>
      <li data-marker="*"><code class="language-plaintext highlighter-rouge">one_gene</code> is a set of all people for whom we want to compute the probability that they have one copy of the gene.</li>
      <li data-marker="*"><code class="language-plaintext highlighter-rouge">two_genes</code> is a set of all people for whom we want to compute the probability that they have two copies of the gene.</li>
      <li data-marker="*"><code class="language-plaintext highlighter-rouge">have_trait</code> is a set of all people for whom we want to compute the probability that they have the trait.</li>
      <li data-marker="*">For any person not in <code class="language-plaintext highlighter-rouge">one_gene</code> or <code class="language-plaintext highlighter-rouge">two_genes</code>, we would like to calculate the probability that they have no copies of the gene; and for anyone not in <code class="language-plaintext highlighter-rouge">have_trait</code>, we would like to calculate the probability that they do not have the trait.</li>
    </ul>
  </li>
  <li data-marker="*">For example, if the family consists of Harry, James, and Lily, then calling this function where <code class="language-plaintext highlighter-rouge">one_gene = {"Harry"}</code>, <code class="language-plaintext highlighter-rouge">two_genes = {"James"}</code>, and <code class="language-plaintext highlighter-rouge">trait = {"Harry", "James"}</code> should calculate the probability that Lily has zero copies of the gene, Harry has one copy of the gene, James has two copies of the gene, Harry exhibits the trait, James exhibits the trait, and Lily does not exhibit the trait.</li>
  <li data-marker="*">For anyone with no parents listed in the data set, use the probability distribution <code class="language-plaintext highlighter-rouge">PROBS["gene"]</code> to determine the probability that they have a particular number of the gene.</li>
  <li data-marker="*">For anyone with parents in the data set, each parent will pass one of their two genes on to their child randomly, and there is a <code class="language-plaintext highlighter-rouge">PROBS["mutation"]</code> chance that it mutates (goes from being the gene to not being the gene, or vice versa).</li>
  <li data-marker="*">Use the probability distribution <code class="language-plaintext highlighter-rouge">PROBS["trait"]</code> to compute the probability that a person does or does not have a particular trait.</li>
</ul>

<p>The <code class="language-plaintext highlighter-rouge">update</code> function adds a new joint distribution probability to the existing probability distributions in <code class="language-plaintext highlighter-rouge">probabilities</code>.</p>

<ul>
  <li data-marker="*">The function accepts five values as input: <code class="language-plaintext highlighter-rouge">probabilities</code>, <code class="language-plaintext highlighter-rouge">one_gene</code>, <code class="language-plaintext highlighter-rouge">two_genes</code>, <code class="language-plaintext highlighter-rouge">have_trait</code>, and <code class="language-plaintext highlighter-rouge">p</code>.
    <ul>
      <li data-marker="*"><code class="language-plaintext highlighter-rouge">probabilities</code> is a dictionary of people as described in the “Understanding” section. Each person is mapped to a <code class="language-plaintext highlighter-rouge">"gene"</code> distribution and a <code class="language-plaintext highlighter-rouge">"trait"</code> distribution.</li>
      <li data-marker="*"><code class="language-plaintext highlighter-rouge">one_gene</code> is a set of people with one copy of the gene in the current joint distribution.</li>
      <li data-marker="*"><code class="language-plaintext highlighter-rouge">two_genes</code> is a set of people with two copies of the gene in the current joint distribution.</li>
      <li data-marker="*"><code class="language-plaintext highlighter-rouge">have_trait</code> is a set of people with the trait in the current joint distribution.</li>
      <li data-marker="*"><code class="language-plaintext highlighter-rouge">p</code> is the probability of the joint distribution.</li>
    </ul>
  </li>
  <li data-marker="*">For each person <code class="language-plaintext highlighter-rouge">person</code> in <code class="language-plaintext highlighter-rouge">probabilities</code>, the function should update the <code class="language-plaintext highlighter-rouge">probabilities[person]["gene"]</code> distribution and <code class="language-plaintext highlighter-rouge">probabilities[person]["trait"]</code> distribution by adding <code class="language-plaintext highlighter-rouge">p</code> to the appropriate value in each distribution. All other values should be left unchanged.</li>
  <li data-marker="*">For example, if <code class="language-plaintext highlighter-rouge">"Harry"</code> were in both <code class="language-plaintext highlighter-rouge">two_genes</code> and in <code class="language-plaintext highlighter-rouge">have_trait</code>, then <code class="language-plaintext highlighter-rouge">p</code> would be added to <code class="language-plaintext highlighter-rouge">probabilities["Harry"]["gene"][2]</code> and to <code class="language-plaintext highlighter-rouge">probabilities["Harry"]["trait"][True]</code>.</li>
  <li data-marker="*">The function should not return any value: it just needs to update the <code class="language-plaintext highlighter-rouge">probabilities</code> dictionary.</li>
</ul>

<p>The <code class="language-plaintext highlighter-rouge">normalize</code> function updates a dictionary of probabilities such that each probability distribution is normalized (i.e., sums to 1, with relative proportions the same).</p>

<ul>
  <li data-marker="*">The function accepts a single value: <code class="language-plaintext highlighter-rouge">probabilities</code>.
    <ul>
      <li data-marker="*"><code class="language-plaintext highlighter-rouge">probabilities</code> is a dictionary of people as described in the “Understanding” section. Each person is mapped to a <code class="language-plaintext highlighter-rouge">"gene"</code> distribution and a <code class="language-plaintext highlighter-rouge">"trait"</code> distribution.</li>
    </ul>
  </li>
  <li data-marker="*">For both of the distributions for each person in <code class="language-plaintext highlighter-rouge">probabilities</code>, this function should normalize that distribution so that the values in the distribution sum to 1, and the relative values in the distribution are the same.</li>
  <li data-marker="*">For example, if <code class="language-plaintext highlighter-rouge">probabilities["Harry"]["trait"][True]</code> were equal to <code class="language-plaintext highlighter-rouge">0.1</code> and <code class="language-plaintext highlighter-rouge">probabilities["Harry"]["trait"][False]</code> were equal to <code class="language-plaintext highlighter-rouge">0.3</code>, then your function should update the former value to be <code class="language-plaintext highlighter-rouge">0.25</code> and the latter value to be <code class="language-plaintext highlighter-rouge">0.75</code>: the numbers now sum to 1, and the latter value is still three times larger than the former value.</li>
  <li data-marker="*">The function should not return any value: it just needs to update the <code class="language-plaintext highlighter-rouge">probabilities</code> dictionary.</li>
</ul>

<p>You should not modify anything else in <code class="language-plaintext highlighter-rouge">heredity.py</code> other than the three functions the specification calls for you to implement, though you may write additional functions and/or import other Python standard library modules. You may also import <code class="language-plaintext highlighter-rouge">numpy</code> or <code class="language-plaintext highlighter-rouge">pandas</code>, if familiar with them, but you should not use any other third-party Python modules.</p>

<h3 id="example-joint-probability">Example Joint Probability</h3>

<p>To help you think about how to calculate joint probabilities, we’ve included below an example.</p>

<p>Consider the following value for <code class="language-plaintext highlighter-rouge">people</code>:</p>

<div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>{
  'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
  'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
  'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
}
</code></pre></div></div>

<p>We will here show the calculation of <code class="language-plaintext highlighter-rouge">joint_probability(people, {"Harry"}, {"James"}, {"James"})</code>. Based on the arguments, <code class="language-plaintext highlighter-rouge">one_gene</code> is <code class="language-plaintext highlighter-rouge">{"Harry"}</code>, <code class="language-plaintext highlighter-rouge">two_genes</code> is <code class="language-plaintext highlighter-rouge">{"James"}</code>, and <code class="language-plaintext highlighter-rouge">has_trait</code> is <code class="language-plaintext highlighter-rouge">{"James"}</code>. This therefore represents the probability that: Lily has 0 copies of the gene and does not have the trait, Harry has 1 copy of the gene and does not have the trait, and James has 2 copies of the gene and does have the trait.</p>

<p>We start with Lily (the order that we consider people does not matter, so long as we multiply the correct values together, since multiplication is commutative). Lily has 0 copies of the gene with probability <code class="language-plaintext highlighter-rouge">0.96</code> (this is <code class="language-plaintext highlighter-rouge">PROBS["gene"][0]</code>). Given that she has 0 copies of the gene, she doesn’t have the trait with probability <code class="language-plaintext highlighter-rouge">0.99</code> (this is <code class="language-plaintext highlighter-rouge">PROBS["trait"][0][False]</code>). Thus, the probability that she has 0 copies of the gene and she doesn’t have the trait is <code class="language-plaintext highlighter-rouge">0.96 * 0.99 = 0.9504</code>.</p>

<p>Next, we consider James. James has 2 copies of the gene with probability <code class="language-plaintext highlighter-rouge">0.01</code> (this is <code class="language-plaintext highlighter-rouge">PROBS["gene"][2]</code>). Given that he has 2 copies of the gene, the probability that he does have the trait is <code class="language-plaintext highlighter-rouge">0.65</code>. Thus, the probability that he has 2 copies of the gene and he does have the trait is <code class="language-plaintext highlighter-rouge">0.01 * 0.65 = 0.0065</code>.</p>

<p>Finally, we consider Harry. What’s the probability that Harry has 1 copy of the gene? There are two ways this can happen. Either he gets the gene from his mother and not his father, or he gets the gene from his father and not his mother. His mother Lily has 0 copies of the gene, so Harry will get the gene from his mother with probability <code class="language-plaintext highlighter-rouge">0.01</code> (this is <code class="language-plaintext highlighter-rouge">PROBS["mutation"]</code>), since the only way to get the gene from his mother is if it mutated; conversely, Harry will not get the gene from his mother with probability <code class="language-plaintext highlighter-rouge">0.99</code>. His father James has 2 copies of the gene, so Harry will get the gene from his father with probability <code class="language-plaintext highlighter-rouge">0.99</code> (this is <code class="language-plaintext highlighter-rouge">1 - PROBS["mutation"]</code>), but will get the gene from his mother with probability <code class="language-plaintext highlighter-rouge">0.01</code> (the chance of a mutation). Both of these cases can be added together to get <code class="language-plaintext highlighter-rouge">0.99 * 0.99 + 0.01 * 0.01 = 0.9802</code>, the probability that Harry has 1 copy of the gene.</p>

<p>Given that Harry has 1 copy of the gene, the probability that he does not have the trait is <code class="language-plaintext highlighter-rouge">0.44</code> (this is <code class="language-plaintext highlighter-rouge">PROBS["trait"][1][False]</code>). So the probability that Harry has 1 copy of the gene and does not have the trait is <code class="language-plaintext highlighter-rouge">0.9802 * 0.44 = 0.431288</code>.</p>

<p>Therefore, the entire joint probability is just the result of multiplying all of these values for each of the three people: <code class="language-plaintext highlighter-rouge">0.9504 * 0.0065 * 0.431288 = 0.0026643247488</code>.</p>
