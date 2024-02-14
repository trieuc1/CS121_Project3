import os
import pickle
from tokenhandler import Token
from document import Document
from posting import Posting
from math import log
import json

class TokenDoesNotExist(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class PostingError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


CORPUS_DIR_NAME = "corpus_state"
TOKENS_FILE_NAME = os.path.join(".", CORPUS_DIR_NAME, "tokens.pkl")
DOC_FILE_NAME = os.path.join(".", CORPUS_DIR_NAME, "documents.pkl")

class Corpus:
    def __init__(self):
        self.tokens = dict()  # {"token": token obj}
        self.postings = dict()
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
        for k, postings in self.postings.items():
            idf = self.get_idf(k)
            temp = []
            for v in postings:
                temp.append(v.get_formatted_posting(idf))
            formatted_tokens[k] = " | ".join(temp)
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
                self.tokens[x] = [doc]
            else:
                self.tokens[x].append(doc)
        self.documents.append(doc)


    def create_all_doc_postings(self):
        """
        This function adds all docs' postings to its corresponding token
        
        Raises PostingError if done unsuccessfully
        """
        for doc in self.documents:
            for token in doc.get_unique_strings():
                token_id = token
                frequency = doc.get_token_frequency(token)
                indices = doc.get_token_indices(token)
                metatag_score = doc.get_metatag_score(token)
                posting = Posting(token_id, doc.get_doc_id(), frequency, indices, metatag_score)
                if token not in self.postings:
                    self.postings[token] = []
                self.postings[token].append(posting)
                if not posting:
                    raise PostingError("ERROR: unable to add posting to token")

    def create_posting(self, doc: Document):
        for token in self.tokens:
            token_id = self.get_token(token).get_id()
            frequency = doc.get_token_frequency(token)
            indices = doc.get_token_indices(token)
            metatag_score = doc.get_metatag_score(token)
            posting = Posting(token_id, doc.get_doc_id, frequency, indices, metatag_score)
            add_posting = self.get_token(token).add_posting(posting)
            if not add_posting:
                raise PostingError("ERROR: unable to add posting to token")

    def get_token(self, token: str) -> Token:
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
        return len(token_obj)


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
        with open("corpus.json", "a") as out_file:
            json.dump(self.get_formatted_corpus(), out_file, indent=6)