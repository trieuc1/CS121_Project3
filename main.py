import atexit
import os
from tokenizer import initialize_corpus 
from corpus import Corpus
import tokenizer
import query

if __name__ == "__main__":
    # Instantiates frontier and loads the last state if exists

    # Registers a shutdown hook to save frontier state upon unexpected shutdown
    # Instantiates a crawler object and starts crawling

    print("Please Select an Option:")
    print("1) Update the Index")
    print("2) Get the Search Results from the given Index")
    print("3) To clear the index")
    print("4) To get all of the terms in the index")
    user_input = input("Please type 1/2/3/4:")

    if user_input == "1":
        corpus = Corpus()
        atexit.register(corpus.dump)
        corpus = initialize_corpus(corpus)
        corpus.dump()
    elif user_input == "2":
        user_input = input("Enter Your Search Query: ")
        query.search_index(user_input)
        print("Finished.")
    elif user_input == "3":
        corpus = Corpus()
        corpus.clear_index()
    elif user_input == "4":
        query.all_terms()
    