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
TAGS = ["h1", "h2", "h3", "h4", "h5", "h6", "b"]

def initialize_corpus(corpus: Corpus) -> Corpus:
    """
    Takes a corpus and propogates it with an index.
    Get folder location from bookkeeper, loops through each one to:
      1. read html
      2. lemmatize
      Seperately:
      1. gets tags
      Then: tokenizes it.
    After finishing, creates the posting
    """
    bookkeeper_ids = list(get_bookkeeper().keys())
    total = len(bookkeeper_ids)
    count = 0
    for book_id in bookkeeper_ids:
        tokenize(corpus, book_id, lemmatize_text(get_text(book_id)), get_tags(book_id), NUMBER_OF_GRAMS)
        print(f"{(count/total)*100:.2f}% \t-- {book_id}", end="\r")
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

def get_text(book_id: str):
    """
    returns all text
    """
    path_string = Path(WEBPAGES_PATH) / book_id
    with open(path_string, 'r', encoding='utf-8') as file:
        content = file.read()
        html = BeautifulSoup(content, 'lxml')
        return html.get_text()

def get_tags(book_id: str):
    """
    returns all words associated with tags. May contain duplicates
    """
    path_string = Path(WEBPAGES_PATH) / book_id
    result = []
    with open(path_string, 'r', encoding='utf-8') as file:
        content = file.read()
        html = BeautifulSoup(content, 'lxml')
        for tag in TAGS:
            for word in html.find_all(tag):
                result.append((word.get_text(), tag))
    return result

def lemmatize_text(html: str):
    """
    Lemmatize text and give type of word
    """
    if html:
        result = []
        pos_tag_list = nltk.pos_tag(word_tokenize(html))
        for pos_tag in pos_tag_list: 
            word = pos_tag[0]
            word_tag = convert_tag(pos_tag[1]) #because its a different tag than lemmetize WordNet
            if word not in STOP_WORDS:        
                if word_tag:
                    result.append(LEMMATIZER.lemmatize(word, pos=word_tag))
                else:
                    result.append(LEMMATIZER.lemmatize(word))
        return result
    else:
        return []


def tokenize(corpus: Corpus, book_id: str, lemmatized: list[str], tags: list[tuple], n: int) -> list:
    """
    Creates a document object with page info
    """
    n_grams = list([lemmatized[0] for i in lemmatized])
    doc = Document(book_id, n_grams, tags)
    corpus.add_document(doc)


if __name__ == "__main__":
    corp = initialize_corpus()
    corp.dump()

    


    





