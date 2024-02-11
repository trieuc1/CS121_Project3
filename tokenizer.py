import json
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from document import Document
from corpus import Corpus


with open("stopwords.txt", "r", encoding='utf-8') as stop_words_file:
    stop_words = stop_words_file.readlines()
    stop_words = [ x.strip().lower() for x in stop_words]

def initialize_corpus():
    corpus = Corpus()
    NUMBER_OF_GRAMS = 2
    bookkeeper_ids = get_bookkeeper_id_set()
    for book_id in bookkeeper_ids:
        text = get_html_text(book_id)
        lemmatized = lemmatize_text(text)
        tokenize(corpus, book_id, lemmatized, NUMBER_OF_GRAMS)
    corpus.create_all_doc_postings()
    return corpus

def get_dict_from_bookkeeper() -> dict:
    with open('WEBPAGES_RAW/bookkeeping.json', encoding='utf-8') as file:
        json_dict = json.load(file)
    return json_dict

def get_bookkeeper_id_set() -> set:
    # set of bookkeeper id's w links that are unique
    unique_ids = set()
    json_dict = get_dict_from_bookkeeper()
    for book_id in json_dict:
        if json_dict[book_id] not in unique_ids:
            unique_ids.add(book_id)
    return unique_ids

def get_html_text(book_id: str) -> str:
    path_string = 'WEBPAGES_RAW/' + book_id
    with open(path_string, 'r', encoding='utf-8') as file:
        content = file.read()
        try:
            return BeautifulSoup(content, "lxml").get_text()
        except Exception as e:
            print(e)
            return ""

def lemmatize_text(html_text: str) -> list:
    lemmatizer = WordNetLemmatizer()
    lemmatized = []
    for x in html_text.split(' '):
        if x not in stop_words:
            lemmatized.append(lemmatizer.lemmatize(x))
    return lemmatized

def tokenize(corpus: Corpus, book_id: str, lemmatized: list, n: int) -> list:
    n_grams = zip(*[lemmatized[i:] for i in range(n)])
    doc = Document(book_id, n_grams)
    corpus.add_document(doc)


    



    


    





