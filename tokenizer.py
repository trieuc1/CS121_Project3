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
TAGS = ["title", "h1", "h2", "h3", "h4", "h5", "h6", "b"]

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
    count = 1
    for book_id in bookkeeper_ids:
        tokenize(corpus, book_id, lemmatize_text(get_text(book_id)), get_tags(book_id), NUMBER_OF_GRAMS)
        print(f"{(count/total)*100:.2f}% \t-- total: {total} \t --completed: {count}     ", end="\r")
        count += 1
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


def get_text(book_id: str) -> str:
    """
    returns all html text
    """
    path_string = Path(WEBPAGES_PATH) / book_id
    with open(path_string, 'rb') as file:
        content = file.read()
        html = BeautifulSoup(content, 'lxml')
        return html.get_text()


def get_tags(book_id: str) -> list[tuple]:
    """
    returns all words associated with tags. May contain duplicates
    """
    path_string = Path(WEBPAGES_PATH) / book_id
    result = []
    lemmatize_result = []
    with open(path_string, 'rb') as file:
        content = file.read()
        html = BeautifulSoup(content, 'lxml')
        for tag in TAGS:
            for word in html.find_all(tag):
                result.append((word.get_text(), tag))
    for word in result:
        for lem_word in lemmatize_text(word[0]):
            lemmatize_result.append((lem_word, word[1]))    
    return lemmatize_result


def lemmatize_text(html: str) ->list[str]:
    """
    Lemmatize text and give type of word
    example output: ["yo, "bro"]
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


def tokenize(corpus: Corpus, book_id: str, lemmatized: list[str], tags: list[tuple], n: int):
    """
    Creates a document object with page info
    """
    n_grams = list(zip(*[lemmatized[i:] for i in range(n)]))
    # if we want the words to be combined instead of separated into a tuple
    n_grams = [(' '.join(i)).strip().lower() for i in n_grams]
    n_tags = list(zip(*[tags[i:] for i in range(n)]))
    new_tags = []
    for tag in n_tags:
        token_string = ""
        token_tags = []
        for x in tag:
            word = x[0]
            tag = x[1]
            token_tags.append(tag)
            token_string += word + ' '
        new_tags.append((token_string.strip().lower(), token_tags))
    doc = Document(book_id, n_grams, new_tags)
    corpus.add_document(doc)


