from tokenhandler import Token
from document import Document
from posting import Posting
from math import log

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
        self.documents = []


    def is_in_corpus(self, token: str) -> bool:
        """
        returns true if the token is already in the token dict
        """
        return self.tokens.get(token, None) is not None


    def add_token(self, token: str) -> bool:
        """
        adds token to the token dict if it hasnt already been added
        """
        if not self.is_in_corpus(token):
            self.tokens[token] = Token(token)


    def add_document(self, doc: Document):
        """
        adds the document obj to the document list and all of its
        unique strings to the tokens dict if the token isnt already
        in the dict
        """
        for x in doc.get_unique_strings():
            self.add_token(x)
        self.documents.append(doc)


    def create_all_doc_postings(self):
        """
        This function adds all docs' postings to its corresponding token
        
        Raises PostingError if done unsuccessfully
        """
        for doc in self.documents:
            for token in doc.get_tokens():
                token_id = self.get_token(token).get_id()
                frequency = doc.get_token_frequency(token)
                indices = doc.get_token_indices(token)
                posting = Posting(token_id, doc.get_doc_id, frequency, indices)
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
