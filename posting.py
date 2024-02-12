from math import log

class Posting:

    posting_id = 0

    def __init__(self, token_id: int, doc_id: int, frequency: int, indices: list,
                  metatag_score: float):
        Posting.posting_id += 1
        self.posting_id = Posting.posting_id
        self.token_id = token_id
        self.doc_id = doc_id
        self.frequency = frequency
        self.indices = indices
        self.metatag_score = metatag_score


    def get_posting_id(self) -> int:
        """
        returns the posting id
        """
        return self.posting_id


    def get_formatted_posting(self, idf: float) -> str:
        """
        returns the formmatted posting
        """
        return f'{self.doc_id}:{self.frequency}:{self.indices}:{self.get_tf_idf(idf)}:{self.metatag_score}'


    def get_doc_id(self) -> int:
        """
        returns the doc id
        """
        return self.doc_id


    def get_token_id(self) -> int:
        """
        returns the token id associated
        """
        return self.token_id


    def get_frequency(self) -> int:
        """
        returns the frequency of the term in the doc
        """
        return self.frequency


    def get_indices(self) -> list:
        """
        returns the indices of when the term occurred in the doc
        """
        return self.indices
    

    def get_metatag_score(self) -> float:
        """
        returns metatag score based on tags of the occurrences of the token
        """
        return self.metatag_score


    def get_tf_idf(self, idf: float) -> float:
        """
        This function calculates the tf-idf score which measures how 
        relevant a word is to a document in a collection of documents
        
        would get idf from Corpus

        the higher the score, the more relevant it is
        """
        return log( 1 + self.frequency) * idf
