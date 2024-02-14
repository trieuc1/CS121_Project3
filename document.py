class Document:
    def __init__(self, bookkeeper_id: int, doc_tokens: list[str], tags: list[tuple()]):
        """
        Constructor for a document
        self.tags example: [("yo hello", ["h1", "h2"])] , where n = 2
        self.doc_tokens: ["yo hello", "hello there"]
        """
        self.doc_id = bookkeeper_id
        self.tags = tags
        self.doc_tokens = doc_tokens
        # set of tuples, where the tuples are tokens ("hello", "there")
        self.unique_strings = set()


    def get_doc_id(self) -> int:
        """
        returns bookkeeper id
        """
        return self.doc_id


    def get_tokens(self) -> list:
        """
        returns the list of document tokens (doesnt have to be unique)
        """
        return self.doc_tokens


    def get_folder_number(self) -> str:
        """
        returns the folder number of the document
        """
        return self.doc_id.split('/')[0]


    def get_file_number(self) -> str:
        """
        returns the file number of the document
        """
        return self.doc_id.split('/')[1]


    def get_unique_strings(self) -> list:
        """
        returns all the unique strings/tokens in a doc
        """
        # index 0 to get word
        for x in self.doc_tokens:
            if x not in self.unique_strings:
                self.unique_strings.add(x)
        return self.unique_strings


    def get_token_frequency(self, token: str) -> int:
        """
        returns the amount of times a token occurred in the doc
        """
        return self.doc_tokens.count(token)


    def get_token_indices(self, token: str) -> list:
        """
        this function returns a list of indices of where the token
        occurred
        """
        indices = []
        for index in range(len(self.doc_tokens)):
            if self.doc_tokens[index] == token:
                indices.append(index)
        return indices

    

    def get_metatag_score(self, token:str) -> float:
        """
        returns a score of importance for each occurance of 
        the token based on the meta tag associated with it

        self.tags example: [("yo hello", ["h1", "h2"])] , where n = 2
        """
        indices = self.get_token_indices(token)
        token_tags = []
        score = 0
        for tup in self.tags:
            if tup[0] == token:
                token_tags += tup[1]
        for tag in token_tags:
            if tag == "title":
                score += 8
            elif tag == "h1":
                score += 7
            elif tag == "h2":
                score += 6
            elif tag == "h3":
                score += 5
            elif tag == "h4":
                score += 4
            elif tag == "h5":
                score += 3
            elif tag == "h6":
                score += 2
            elif tag == "b":
                score += 1.5
        score += len(indices) - len(token_tags)
        return score / len(indices)
        
