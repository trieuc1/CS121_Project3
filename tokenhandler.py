from posting import Posting

class PostingDoesNotExist(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Token:
    token_id = 0

    def __init__(self, token_string: str):
        Token.token_id += 1
        self.token_id = Token.token_id
        self.token_string = token_string
        self.postings = []
    
    def formatted_postings(self, idf: float):
        formatted_postings = []
        for post in self.postings:
            formatted_postings.append(post.get_formatted_posting(idf))
        return formatted_postings


    def get_token_id(self) -> int:
        """
        returns the token id
        """
        return self.token_id


    def get_token_string(self) -> str:
        """
        returns the token string
        """
        return self.token_string


    def get_postings(self) -> list:
        """
        returns the list of Posting objects
        """
        return self.postings


    def get_posting_by_id(self, posting_id: int) -> Posting:
        """
        Returns the posting object based on the posting id given
        """
        for x in self.postings:
            if x.get_id() == posting_id:
                return x
        raise PostingDoesNotExist("ERROR: Posting doesn't exist.")


    def add_posting(self, post: Posting) -> bool:
        """
        adds a posting object to the postings list
        """
        self.postings.append(post)
        return True
