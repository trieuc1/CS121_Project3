import json
import nltk
import spacy
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from corpus import Corpus
from document import Document

#to use spacy you have to download the model
#first pip install spacy
#then python -m spacy download en_core_web_sm (to download the model)
#Below is all of the stop words from nltk + spacy

STOP_WORDS = set(list(stopwords.words('english')) + list(spacy.load('en_core_web_sm').Defaults.stop_words))
NUMBER_OF_GRAMS = 2

def initialize_corpus():
    corpus = Corpus()
    bookkeeper_ids = get_bookkeeper_id_set()

    for book_id in bookkeeper_ids:
        # text = get_html_text(book_id)
        tags = get_word_tags(book_id)
        lemmatized = lemmatize_text(tags)
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

# def get_html_text(book_id: str) -> str:
#     path_string = 'WEBPAGES_RAW/' + book_id

#     with open(path_string, 'r', encoding='utf-8') as file:
#         content = file.read()

#         try:
#             html_text = BeautifulSoup(content, "lxml").get_text()
#             return html_text
#         except (Exception) as error:
#             print(error)
#             return ""

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

def get_word_tags(book_id: str) -> list:
    """
    returns list of tuple of words and their associated tags from html
    
    [(word, meta_tag)]
    """
    path_string = 'WEBPAGES_RAW/' + book_id

    with open(path_string, 'r', encoding='utf-8') as file:
        content = file.read()
        html_w_tags = BeautifulSoup(content, 'html.parser')
        tags = []
        for element in html_w_tags.find_all():
            if hasattr(element, 'text'):
                text = element.text.strip()
                words = text.split()
                for word in words:
                    tags.append((word.lower(), element.name))
    return tags


def lemmatize_text(tags: list) -> list:
    lemmatized = []
    html_list = [word[0] for word in tags]
    html_text = html_list.join(" ")
    
    if html_text:
        html_text_pos = nltk.pos_tag(word_tokenize(html_text))
        lemmatizer = WordNetLemmatizer()

        for i in range(len(html_text_pos)):
            word_tuple = html_text_pos[i]
            word = word_tuple[0]
            word_tag = convert_tag(word_tuple[1]) #because its a different tag than lemmetize WordNet
    
            if word not in STOP_WORDS:
        
                if word_tag:
                    lemmatized.append((lemmatizer.lemmatize(word, pos=word_tag), tags[i][1]))
                else:
                    lemmatized.append((lemmatizer.lemmatize(word), tags[i][1]))
    
    return lemmatized


def tokenize(corpus: Corpus, book_id: str, lemmatized: list, n: int) -> list:
    n_grams = zip(*[lemmatized[i:] for i in range(n)])
    doc = Document(book_id, n_grams)
    corpus.add_document(doc)


    



    


    





