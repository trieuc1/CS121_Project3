import atexit
from tokenizer import initialize_corpus 
from corpus import Corpus, insert_json
from flask import Flask, render_template, request, Response
import query

# need to do pip install flask

app = Flask(__name__)
app.secret_key = None

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/search', methods=['POST', 'GET'])
def process_form():
    if request.method == 'POST':
        search_input = request.form['search_input'].lower().strip()
        app.secret_key = search_input
    elif request.method == 'GET':
        search_input = request.args.get('search_input',default=app.secret_key, type=str).strip()

    results, doc_id_results = query.query(search_input)
    num_results = len(results)

    page = request.args.get('page', default=1, type=int)
    print(search_input, page)
    word_search = search_input
    per_page = 50
    offset = (page - 1) * per_page
    paginated_results = results[offset:offset + per_page]
    paginated_doc_ids = doc_id_results[offset:offset + per_page]

    return_results = []
    for link, doc_id in zip(paginated_results, paginated_doc_ids):
        title = query.get_query_details(doc_id)
        return_results.append({'link': link, 'title': title, 'id': doc_id})

    num_pages = (num_results + per_page - 1) // per_page

    return render_template('results.html', results=return_results, num_results=num_results, page=page, num_pages=num_pages, word_search=word_search)

        
@app.route('/show/<path:url>')
def dynamic_page(url):
    print(f"User requests for page url: {url}")
    html_info = query.get_html_info(url)
    return render_template('tmpResult.html', html_content=html_info)

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

    #     results = query.query(user_input)
    #     for link in results:
    #         print(link)
    #     print("Finished.")
    # elif user_input == "3":
    #     corpus = Corpus()
    #     corpus.clear_index()
    # elif user_input == "4":
    #     query.all_terms()
    # elif user_input == "5":
    #     insert_json()
    app.run(host='127.0.0.1', port=5000)
    