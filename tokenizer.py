import json
import nltk
import spacy
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from corpus import Corpus
from document import Document
from pathlib import Path
import time
#to use spacy you have to download the model
#first pip install spacy
#then python -m spacy download en_core_web_sm (to download the model)
#Below is all of the stop words from nltk + spacy

STOP_WORDS = set(list(stopwords.words('english')) + list(spacy.load('en_core_web_sm').Defaults.stop_words))
NUMBER_OF_GRAMS = 1
WEBPAGES_PATH = "WEBPAGES_RAW"
LEMMATIZER = WordNetLemmatizer()

def initialize_corpus(corpus: Corpus) -> Corpus:
    bookkeeper_ids = list(get_bookkeeper().keys())
    total = len(bookkeeper_ids)
    count = 0
    for book_id in bookkeeper_ids:
        start = time.time()
        word_list = get_formatted_text(book_id)
        tokenize(corpus, book_id, word_list, NUMBER_OF_GRAMS)
        end = time.time()
        print(f"{(count/total)*100:.2f}% \t-- {book_id} \t -- {end-start:.2f}s", end="\n")
        count += 1
    corpus.create_all_doc_postings()
    return corpus

def get_bookkeeper() -> dict:
    # set of bookkeeper id's w links that are unique
    bookkeeper_path = Path(WEBPAGES_PATH) / "bookkeeping.json"
    with open(bookkeeper_path, encoding='utf-8') as file:
        json_dict = json.load(file)

    return json_dict

def convert_tag(tag: str) -> str:
    if tag.startswith('N'):
        return 'n'  # noun
    elif tag.startswith('V'):
        return 'v'  # verb
    elif tag.startswith('J'):
        return 'a'  # adjective
    elif tag.startswith('R'):
        return 'r'  # adverb
    else:
        return None

def get_word_tags(book_id: str):
    """
    returns list of tuple of words and their associated tags from html
    [(word, meta_tag)]
    """
    path_string = Path(WEBPAGES_PATH) / book_id
    with open(path_string, 'r', encoding='utf-8') as file:
        content = file.read()
        html_w_tags = BeautifulSoup(content, 'html.parser')
        for element in html_w_tags.find_all():
            if hasattr(element, 'text'):
                text = element.text.strip()
                words = text.split()
                for word in words:
                    yield ((word.lower(), element.name))


def lemmatize_text(tags: tuple):
    word = tags[0]
    element = tags[1]
    if word:
        pos_tag_list = nltk.pos_tag(word_tokenize(word))
        for pos_tag in pos_tag_list: 
            word = pos_tag[0]
            word_tag = convert_tag(pos_tag[1]) #because its a different tag than lemmetize WordNet
            if word not in STOP_WORDS:        
                if word_tag:
                    yield (LEMMATIZER.lemmatize(word, pos=word_tag), element)
                else:
                    yield (LEMMATIZER.lemmatize(word), element)

def get_formatted_text(book_id: str):
    result = []
    for i in get_word_tags(book_id):
        for j in lemmatize_text(i):
            result.append(j)
    return result


def tokenize(corpus: Corpus, book_id: str, lemmatized: list, n: int) -> list:
    n_grams = list([lemmatized[0] for i in lemmatized])
    doc = Document(book_id, n_grams)
    corpus.add_document(doc)


if __name__ == "__main__":
    corp = initialize_corpus()
    corp.dump()

    


    





