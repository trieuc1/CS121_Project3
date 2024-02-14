import atexit
import os
from tokenizer import initialize_corpus 
from corpus import Corpus
import tokenizer

if __name__ == "__main__":
    # Instantiates frontier and loads the last state if exists

    # Registers a shutdown hook to save frontier state upon unexpected shutdown
    # Instantiates a crawler object and starts crawling
    if (os.path.isfile("corpus.json") == False):
        corpus = Corpus()
        atexit.register(corpus.dump)
        corpus = initialize_corpus(corpus)
        corpus.dump()
    
    print("Search: ")
    user_query = input()
    