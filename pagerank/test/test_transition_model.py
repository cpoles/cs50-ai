from pagerank import transition_model
from pytest import approx

corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
corpus_no_link = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {}}

damping = 0.85


# tests for no, one and 2 links

# no outgoing links
def test_transition_model_no_link_damping():
    assert transition_model(corpus_no_link, '3.html', damping) ==  {'1.html': 1/3, '2.html': 1/3, '3.html': 1/3}

# one link
def test_transition_model_one_link_damping():
    assert transition_model(corpus, '2.html', damping) ==  {'1.html': approx(0.15/3), '2.html': approx(0.15/3), '3.html': 0.85 + (0.15/3)}

# two links
def test_transition_model_two_links_damping():
    assert transition_model(corpus, '1.html', damping) ==  {"1.html": approx(0.05), "2.html": approx(0.475), "3.html": approx(0.475)}