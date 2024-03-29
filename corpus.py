from document import Document
from posting import Posting
from tokenhandler import Token
from math import log
import json
import mongodb
from pathlib import Path

DATASAVE = "mongodb+srv://proj3Cluster:idepZy2mBvChOvan@projectcluster.5idbqzt.mongodb.net/"
DATASAVE_TWO = "mongodb+srv://jasonhw3:EBl154EMmvjllXLL@cluster0.tgq8vgu.mongodb.net/?retryWrites=true&w=majority"
TWO_GRAM_SAVE = "mongodb+srv://jasonhw3:xw24GXGcWhyi31Ly@cluster0.57kbxtr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
TWO_GRAM_SAVE_TWO = "mongodb+srv://jasonhw3:llZUsmhqHCeNNCwl@cluster0.tulx44z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE = "Database"
COLLECTION = "Collection"

class TokenDoesNotExist(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class PostingError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Corpus:
    def __init__(self):
        self.tokens = dict()  # {"token": token obj}
        self.postings = dict() # {"word": [posting obj, posting obj, ...]}
        self.documents = []
    
    def get_formatted_corpus(self) -> dict:
        """
        returns a dictionary where the key is the token string and
        its value is a list of formatted postings

        {"token": [formatted postings]}
        """
        if len (self.postings) == 0:
            self.create_all_doc_postings()
        formatted_tokens = dict()
        for token_str, token_obj in self.tokens.items():
            idf = self.get_idf(token_str)
            temp = []
            for post in token_obj.get_postings():
                temp.append(post.get_formatted_posting(idf))
            formatted_tokens[token_str] = " | ".join(temp)
        return formatted_tokens


    def is_in_corpus(self, token: str) -> bool:
        """
        returns true if the token is already in the token dict
        """
        return self.tokens.get(token, None) is not None


    def add_document(self, doc: Document):
        """
        adds the document obj to the document list and all of its
        unique strings to the tokens dict if the token isnt already
        in the dict
        """
        for x in doc.get_unique_strings():
            if x not in self.tokens:
                self.tokens[x] = Token(x)
        self.documents.append(doc)


    def create_all_doc_postings(self):
        """
        This function creates and adds all docs' postings to its
        corresponding token
        
        Raises PostingError if done unsuccessfully
        """
        total = len(self.documents)
        count = 1
        print("\nPosting!")
        for doc in self.documents:
            self.create_posting(doc)
            print(f"{(count/total)*100:.2f}% \t-- total: {total} \t --completed: {count}     ", end="\r")
            count += 1
        print()

    def create_posting(self, doc: Document):
        """
        creates all postings based off a Document obj content
        """
        for token in doc.get_unique_strings():
            token_id = self.get_token(token).get_token_id()
            frequency = doc.get_token_frequency(token)
            indices = doc.get_token_indices(token)
            metatag_score = doc.get_metatag_score(token)
            posting = Posting(token_id, doc.get_doc_id(), frequency, indices, metatag_score)
            add_posting = self.get_token(token).add_posting(posting)
            if not add_posting:
                raise PostingError("ERROR: unable to add posting to token")

    def get_token(self, token: str):
        """
        this function returns the token obj based on the token string
        """
        returned_token = self.tokens.get(token, None)
        if returned_token is None:
            raise TokenDoesNotExist("ERROR: The searched token doesn't exist.")
        return returned_token


    def get_all_docs(self) -> list[Document]:
        return self.documents


    def get_doc_frequency(self, token: str) -> int:
        """
        this function returns the frequency of a token in a document
        """
        token_obj = self.tokens.get(token)
        return len(token_obj.get_postings())


    def get_idf(self, token: str) -> float:
        """
        This function returns the IDF score which tells us how common
        or rare a word is in the corpus
        
        closer to 0 -> more common
        """
        return log(len(self.documents)/ self.get_doc_frequency(token))

    def dump(self):
        """
        Dumps contents into a JSON
        """
        dict_list = []
        formmated_corpus = self.get_formatted_corpus()
        for data in formmated_corpus.items():
            dict_list.append({data[0]: data[1]})        
        with open("corpus.json", "w", encoding="utf-8") as out_file:
            json.dump(formmated_corpus, out_file, indent=6, ensure_ascii=False)

    def clear_index(self):
        mongodbInstance = mongodb.DataSave(DATASAVE, DATABASE, COLLECTION)
        mongodbInstance.remove_collection()
        mongodbInstance_two = mongodb.DataSave(DATASAVE_TWO, DATABASE, COLLECTION)
        mongodbInstance_two.remove_collection()
    
    def clear_index_n_gram(self):
        mongodbInstance = mongodb.DataSave(TWO_GRAM_SAVE, DATABASE, COLLECTION)
        mongodbInstance.remove_collection()
        mongodbInstance = mongodb.DataSave(TWO_GRAM_SAVE_TWO, DATABASE, COLLECTION)
        mongodbInstance.remove_collection()

    
    
def insert_json(path="corpus.json"):
    """
    Uploads json to corpus
    """
    if (Path(path).is_file() == False):
        print("Path isn't a file")
        return
    corpus_dict = {}
    dict_list = []
    with open(path, encoding="utf-8") as in_file:
        corpus_dict = json.load(in_file)
    
    total = len(corpus_dict)
    count = 0
    for key, value in corpus_dict.items():
        dict_list.append({key: value})
        if len(dict_list) == 35000:
            print(f"{(count/total)*100:.2f}% \t-- total: {count} \t --completed: {total}     ", end="\r")
            try:
                mongodbInstance = mongodb.DataSave(DATASAVE, DATABASE, COLLECTION)
                mongodbInstance.insert_all(dict_list)
            except Exception as e:
                print("Full, moving onto the second database")
                mongodbInstance = mongodb.DataSave(DATASAVE_TWO, DATABASE, COLLECTION)
                mongodbInstance.insert_all(dict_list)

            count += 35000
            dict_list.clear()
    try:
        mongodbInstance = mongodb.DataSave(DATASAVE, DATABASE, COLLECTION)
        mongodbInstance.insert_all(dict_list)
    except Exception as e:
        print("Full, moving onto the second database")
        mongodbInstance = mongodb.DataSave(DATASAVE_TWO, DATABASE, COLLECTION)
        mongodbInstance.insert_all(dict_list)

    
def insert_n_gram_json(path="2_gram_corpus.json"):
    """
    Uploads json to corpus
    """
    
    if (Path(path).is_file() == False):
        print("Path isn't a file")
        return
    corpus_dict = {}
    dict_list = []
    with open(path, encoding="utf-8") as in_file:
        corpus_dict = json.load(in_file)
    
    total = len(corpus_dict)
    count = 0
    mongodbInstance = mongodb.DataSave(TWO_GRAM_SAVE, DATABASE, COLLECTION)
    for key, value in corpus_dict.items():
        dict_list.append({key: value})
        print(f"{(count/total)*100:.2f}% \t-- total: {count} \t --completed: {total}     ", end="\r")
        if len(dict_list) == 35000:
            try:
                mongodbInstance.insert_all(dict_list)
            except Exception as e:
                print("Full, moving onto the second database")
                mongodbInstance = mongodb.DataSave(TWO_GRAM_SAVE_TWO, DATABASE, COLLECTION)
                mongodbInstance.insert_all(dict_list)

            dict_list.clear()
        count += 1
    try:
        mongodbInstance = mongodb.DataSave(TWO_GRAM_SAVE, DATABASE, COLLECTION)
        mongodbInstance.insert_all(dict_list)
    except Exception as e:
        print("Full, moving onto the second database")
        mongodbInstance = mongodb.DataSave(TWO_GRAM_SAVE_TWO, DATABASE, COLLECTION)
        mongodbInstance.insert_all(dict_list)