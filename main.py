import atexit
from tokenizer import initialize_corpus 
from corpus import Corpus, insert_json
from flask import Flask, render_template, request
import query

# need to do pip install flask

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def process_form():
    search_input = request.form['search_input'].lower().strip()
    results = query.search_index(search_input)
    num_results = f'Total Number of Results: {len(results)}'
    return render_template('results.html', results=results, num_results=num_results)


if __name__ == "__main__":
    # Instantiates frontier and loads the last state if exists

    # Registers a shutdown hook to save frontier state upon unexpected shutdown
    # Instantiates a crawler object and starts crawling

    # print("Please Select an Option:")
    # print("1) Update the Index")
    # print("2) Get the Search Results from the given Index")
    # print("3) To clear the index")
    # print("4) To get all of the terms in the index")
    # print("5) To upload JSON file to the index")
    # user_input = input("Please type 1/2/3/4/5:")

    # if user_input == "1":
    #     corpus = Corpus()
    #     atexit.register(corpus.dump)
    #     corpus = initialize_corpus(corpus)
    #     atexit.unregister(corpus.dump)
    #     corpus.dump()
    # elif user_input == "2":
    #     user_input = input("Enter Your Search Query: ").lower().strip()

    #     results = query.search_index(user_input)
    #     print(results)
    #     print("Finished.")
    # elif user_input == "3":
    #     corpus = Corpus()
    #     corpus.clear_index()
    # elif user_input == "4":
    #     query.all_terms()
    # elif user_input == "5":
    #     insert_json()
    app.run(host='127.0.0.1', port=5000)
    