class Document:
    def __init__(self, bookkeeper_id: int, doc_tokens: list[str], tags: list[tuple]):
        """
        Constructor for a document
        self.tags example: [("yo hello", ["h1", "h2"])] , where n = 2
        self.doc_tokens: ["yo hello", "hello there"]
        """
        self.doc_id = bookkeeper_id
        self.tags = tags
        self.doc_tokens = doc_tokens
        # set of tuples, where the tuples are tokens ("hello", "there")
        self.unique_strings = set(doc_tokens)
        self.word_count = dict()
        self.word_indices = dict()
        self.generate_word_info()
    
    def generate_word_info(self):
        """
        Creates dictionary with frequency of word in doc
        """
        for word in self.unique_strings:
            self.word_count[word] = 0
            self.word_indices[word] = []
        for index in range(len(self.doc_tokens)):
            word = self.doc_tokens[index]
            self.word_count[word] += 1
            self.word_indices[word].append(index)

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
        return self.unique_strings


    def get_token_frequency(self, token: str) -> int:
        """
        returns the amount of times a token occurred in the doc
        """
        return self.word_count[token]


    def get_token_indices(self, token: str) -> list:
        """
        this function returns a list of indices of where the token
        occurred
        """
        return self.word_indices[token]

    

    def get_metatag_score(self, token:str) -> float:
        """
        returns a score of importance for each occurance of 
        the token based on the meta tag associated with it

        self.tags example: [("yo hello", ["h1", "h2"])] , where n = 2
        """
        indices = self.word_count[token]
        score = 0
        if len(token.split(" ")) >= 2:
            tags_matrix = {word: {} for word in token.split(" ")}
            for word, html_tag in self.tags:
                if word in tags_matrix.keys():
                    html_tag = html_tag[0]
                    if html_tag not in tags_matrix[word].keys():
                        tags_matrix[word][html_tag] = 1
                    else:
                        tags_matrix[word][html_tag] += 1
            # Now it should be this format:
            # {
            #     "test": {
            #         "p": 3,
            #         "title": 2
            #     }
            #     "bro": {
            #         "p": 1
            #     }
            # }
            list_of_tags = []
            for word, tag_dict in tags_matrix.items():
                list_of_tags.append(set(tag_dict.keys()))
            shared_tags = set.intersection(*list_of_tags)
            for tag in shared_tags:
                min_count = 0
                for word, tag_dict in tags_matrix.items():
                    if min_count == 0:
                        min_count = tags_matrix[word][tag]
                    else:
                        min_count = min(tags_matrix[word][tag], min_count)
                score += 2 * min_count
        else:
            for tup in self.tags:
                if tup[0] == token:
                    score += 2
        score += indices - (score / 2)
        return score / indices
        
