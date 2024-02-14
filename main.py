import atexit
from tokenizer import initialize_corpus
from corpus import Corpus

if __name__ == "__main__":
    # Instantiates frontier and loads the last state if exists

    # Registers a shutdown hook to save frontier state upon unexpected shutdown
    
    # Instantiates a crawler object and starts crawling
    corpus = Corpus()
    atexit.register(corpus.dump)
    corpus = initialize_corpus(corpus)
    corpus.dump()
