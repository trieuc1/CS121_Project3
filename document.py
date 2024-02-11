class Document:
    doc_id = 0

    def __init__(self, bookkeeper_id: int, doc_tokens: list):
        Document.doc_id += 1
        self.doc_id = Document.doc_id
        self.doc_tokens = doc_tokens
        self.unique_strings = set()
        self.bookkeeper_id = bookkeeper_id


    def get_doc_id(self) -> int:
        """
        this function returns the documents id
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
        return self.bookkeeper_id.split('/')[0]


    def get_file_number(self) -> str:
        """
        returns the file number of the document
        """
        return self.bookkeeper_id.split('/')[1]

    def get_bookkeeper_id(self) -> str:
        """
        returns bookkeeper id
        """
        return self.bookkeeper_id
    
    def get_meta_weight(self) -> float:

        # TODO: fill in this function
        return 0.0



    def get_unique_strings(self) -> list:
        """
        returns all the unique strings/tokens in a doc
        """
        for x in self.doc_tokens:
            if x not in self.unique_strings:
                self.unique_strings.add(x)
        return self.unique_strings


    def get_token_frequency(self, token: str) -> int:
        """
        returns the amount of times a token occurred in the doc
        """
        return self.doc_tokens.count(token)


    def get_token_indices(self, token:str) -> list:
        """
        this function returns a list of indices of where the token
        occurred
        """
        indices = []
        for index in range(len(self.doc_tokens)):
            if self.doc_tokens[index] == token:
                indices.append(index)
        return indices
