import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)
    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files_content = dict()
    # traverse directory, read file and add to dictionary
    for filename in os.listdir(directory):
        with open(os.path.sep.join([directory, filename])) as f:
            contents = f.read()
            files_content[filename] = contents
    
    return files_content

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # Load stopwords
    stopwords = nltk.corpus.stopwords.words("english")

    # Lowercase word. 
    return [word
            for word in nltk.word_tokenize(document.lower())
                # If word is neither a stopword nor punctuation, add it to the list
                if not (word in stopwords or word in string.punctuation)] 
                                    


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # Set of all words in corpus
    words = {word for filename in documents for word in documents[filename]}

    idfs = dict()
    
    # Loop through words
    for word in words:
        # Number of documents the word appears in
        f = sum(word in documents[filename] for filename in documents)
        # Calculate idf and update dictionary
        idf = math.log(len(documents) / f)
        idfs[word] = idf

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    tfids = dict()

    # Loop through files
    for filename in files:
        tfids[filename] = 0
        # Loop through query words
        for word in query:
            # If word in document, calculate its tfid
            if word in files[filename]:
                tf = files[filename].count(word)
                # Update document's tfid
                tfids[filename] += (tf * idfs[word])
    
    # Sort tfids
    tfids = dict(sorted(tfids.items(), key=lambda item: item[1], reverse=True))

    return list(tfids.keys())[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    # Keep track of number of query words in the sentence, sentence length, idf and qme for ranking
    sentences_stats = {sentence: {'idf': 0, 'q_words': 0, 'qme': 0} for sentence in sentences}

    # Loop through sentences
    for sentence in sentences:
        # Loop through each word in query
        for word in query:
            # If query word in the sentence, update idf and q_words
            if word in sentences[sentence]:
                sentences_stats[sentence]['idf'] += idfs[word]
                sentences_stats[sentence]['q_words'] += sentence.count(word)

        # Calculate qme
        sentences_stats[sentence]['qme'] = sentences_stats[sentence]['q_words'] / len(nltk.word_tokenize(sentence))

    
    # Sort by idf then qme
    ranking = sorted([sentence for sentence in sentences], 
                        key=lambda s: (sentences_stats[s]['idf'], sentences_stats[s]['qme']), reverse=True)

    return ranking[:n]

if __name__ == "__main__":
    main()
