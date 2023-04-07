import os
import random
import re
import sys
from copy import deepcopy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # handle case with no outgoing pages from page
    if not corpus[page]:
        # assign equal probability to all pages
        return dict.fromkeys(corpus.keys(), 1 / len(corpus))

    # get links
    links = corpus[page]

    # create model from pages
    model = dict.fromkeys(corpus.keys(), 0)
    
    # probabilities
    random_link_prob = (1 - DAMPING) / len(corpus)

    link_prob = damping_factor / len(links)

    # assign probabilities
    for pg in model:
        # add randomness to all pages
        model[pg] += random_link_prob
        # if pg is a link on the page, add link prob
        if pg in corpus[page]:
            model[pg] += link_prob
            
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    counter = dict.fromkeys(corpus.keys(), 0)

    # first sample
    page = random.choice(list(corpus.keys()))

    counter[page] += 1

    # generate other n-1 samples
    for _ in range(0, n - 1):
        # get the probs from the transition model
        tr_model = transition_model(corpus, page, damping_factor)

        # get pages and probabilities from the tr model
        pages, probs = list(tr_model.keys()), tr_model.values()
        # get next page
        page = random.choices(pages, weights=probs)[0]
        # update counter
        counter[page] += 1

    # calculate the prob for each page
    for pg in counter:
        counter[pg] /= n

    # print(f"The sum is: {sum(counter.values()):.4f}")

    return counter


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # assign equal probabilities 
    pagerank = dict.fromkeys(corpus.keys(), 1/ len(corpus))
    newrank = dict.fromkeys(corpus.keys(), 1/ len(corpus))

    while True:
        # monitor current rank
        current_rank = list(pagerank.values())

        for page in corpus:
            pri = 0
            for lpage in corpus:
                # page is incoming link from lpage
                if page in corpus[lpage]:
                    pri += pagerank[lpage] / len(corpus[lpage])
                # if there are no links in lpage
                if not corpus[lpage]:
                    pri += pagerank[lpage] / len(corpus)

            # calculate page rank
            page_rank = (1 - damping_factor) / len(corpus) + damping_factor * pri

            # update newrank
            newrank[page] = page_rank

        # update pagerank
        pagerank = deepcopy(newrank)

        # monitor new_rank
        new_rank = list(newrank.values())

        # compare ranks for precision
        if all([abs(cr - nr) < 0.001 for cr, nr in zip(current_rank, new_rank)]):
            # print(f"Sum is {sum(pagerank.values())}")
            return pagerank
            

if __name__ == "__main__":
    main()
