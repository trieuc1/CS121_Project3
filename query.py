from collections import namedtuple
import json
import mongodb
from pathlib import Path
import numpy as np

DATASAVE = "mongodb+srv://proj3Cluster:idepZy2mBvChOvan@projectcluster.5idbqzt.mongodb.net/"
DATASAVE_TWO = "mongodb+srv://jasonhw3:EBl154EMmvjllXLL@cluster0.tgq8vgu.mongodb.net/?retryWrites=true&w=majority"
DATABASE = "Database"
COLLECTION = "Collection"
BOOKKEEPER_PATH = Path("WEBPAGES_RAW") / Path("bookkeeping.json")
CORPUS_SIZE = 37424
Stats = namedtuple('Stats', 'count, position, idf, metatag')

class LoadBookMark:
    
    def __init__(self):
        self.jsonResult = None
        self.load_bookmark_json()
    
    def load_bookmark_json(self):
        if self.jsonResult == None:
            with open(BOOKKEEPER_PATH, "r", encoding="utf-8") as bookkeeper_file:
                self.jsonResult = json.loads(bookkeeper_file.read())
    
    def find_query(self, id_input:str):
        """
        returns the link associated with the doc id
        """
        return self.jsonResult[id_input]


def search_all_index():
    """
    Loads the index!
    """
    mongodbInstance = mongodb.DataSave(DATASAVE, DATABASE, COLLECTION)
    for document in mongodbInstance.retreive_all_data():
        # Remove the '_id' field from the document
        del document['_id']
        # Iterate over key-value pairs in the document
        for term, index in document.items():
            string_term = ""
            print(f"---------------------------Current Word: {term}------------------------")
            res = index.split(" | ")
            for i in res:
                string_term += i[:i.find(":")] + " "
            print(string_term)
            print(f"-----------------------------------------------------------------------")
    
    mongodbInstance_two = mongodb.DataSave(DATASAVE_TWO, DATABASE, COLLECTION)
    for document in mongodbInstance_two.retreive_all_data():
        # Remove the '_id' field from the document
        del document['_id']
        # Iterate over key-value pairs in the document
        for term, index in document.items():
            string_term = ""
            print(f"---------------------------Current Word: {term}------------------------")
            res = index.split(" | ")
            for i in res:
                string_term += i[:i.find(":")] + " "
            print(string_term)
            print(f"-----------------------------------------------------------------------")


def search_index(term_input: str) -> str:
    """
    Loads the specific queried Index and prints the links out
    """
    mongodbInstance = mongodb.DataSave(DATASAVE, DATABASE, COLLECTION)
    mongodbInstance_two = mongodb.DataSave(DATASAVE_TWO, DATABASE, COLLECTION)

    try:
        query_result = mongodbInstance.get_query(term_input)[term_input]
    except TypeError:
        print("Unable to Search for the Query. Does not Exist. Checking 2nd Database")
        try:
            query_result = mongodbInstance_two.get_query(term_input)[term_input]
        except TypeError:
            print("Unable to search for term in the 2nd database. Term does not exist.")
            return

    #print(f"Searching for {term_input}...")
    #loaded_bookmarks = LoadBookMark()
    #res = query_result.split(" | ")
    #list_of_document_id = [ i[:i.find(":")] for i in res]
    #rank(term_input, res)
    #return [loaded_bookmarks.find_query(id) for id in list_of_document_id]
    return query_result
    # for id in list_of_document_id:
    #     print(f"{loaded_bookmarks.find_query(id)}")
    
def all_terms():
    """
    prints out all terms stored in both databases
    """
    mongodbInstance = mongodb.DataSave(DATASAVE, DATABASE, COLLECTION)
    mongodbInstance_two = mongodb.DataSave(DATASAVE_TWO, DATABASE, COLLECTION)
    list_of_terms = []
    for document in mongodbInstance.retreive_all_data():
        # Remove the '_id' field from the document
        del document['_id']
        # Iterate over key-value pairs in the document
        for term in document.keys():
            list_of_terms.append(term)

    for document in mongodbInstance_two.retreive_all_data():
        # Remove the '_id' field from the document
        del document['_id']
        # Iterate over key-value pairs in the document
        for term in document.keys():
            list_of_terms.append(term)
        
    print(list_of_terms)

def cosine(index: dict, inverted_index: dict, term_input: str) -> list[tuple]:
    """
    Calculates and sorts doc+id according to idf.tf scores
    """
    # Get query vector
    term_query = term_input.split()
    term_idf = {}
    # get tf, store in term_idf, to be replaced
    for term in term_query:
        if term not in term_idf:
            term_idf[term] = 1
        else:
            term_idf[term] += 1
    # calculated idf for query
    for term, value in term_idf.items():
        term_idf[term] = np.log(CORPUS_SIZE / len(inverted_index[term])) * (1+np.log(value))
    # query vector
    query_vector = np.fromiter(term_idf.values(), dtype=float)
    query_vector = query_vector / np.linalg.norm(query_vector)
    
    # get score for each doc
    scores = []
    for doc_id in index.keys():
        score_vector = np.empty(len(term_idf.keys()))
        for score_index, term in enumerate(term_query):
            if term in index[doc_id]:
                score_vector[score_index] = index[doc_id][term].idf
        score_vector = score_vector / np.linalg.norm(score_vector)
        doc_score = np.dot(query_vector, score_vector)
        scores.append([doc_id, doc_score])
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return sorted_scores

def tf_idf_scoring(index: dict, term_input: str)-> list[tuple]:
    """
    Scores using the sum of tf.idf values, then normalized
    """
    # Get query vector
    term_query = term_input.split()
    # get tf, store in term_idf, to be replaced
    # get sum tf-idf score for each doc
    scores = []
    tf_idf_list = np.empty(len(index))
    for count, doc_id in enumerate(index.keys()):
        total = 0
        for term in term_query:
            if term in index[doc_id]:
                total += index[doc_id][term].idf
        scores.append([doc_id, total])
        tf_idf_list[count] = total
    # normalize tf-idf
    norm_factor = np.linalg.norm(tf_idf_list)
    for i in range(len(scores)):
        scores[i][1] = scores[i][1] / norm_factor
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return sorted_scores

def query(term_input: str) -> list[str]:
    loaded_bookmarks = LoadBookMark()
    term_set = set(term_input.split())
    index = {}
    inverted_index = {}
    # Structure for index
    # "folder": {"term": stats, "computer": stats(count=4,position=[3],idf=.23,metatag=1)}
    # inverted index is as expected
    for term in term_set:
        query_result = search_index(term)
        if query_result is None:
            term_set.discard(term)
        else:
            res = query_result.split(" | ")
            inverted_index[term] = res
            for doc in res:
                doc_info = doc.split(":")
                doc_id = doc_info[0]
                position_list = doc_info[2].strip("[").strip("]").split(",")
                position_list = [int(i) for i in position_list]
                doc_stats = Stats(count=int(doc_info[1]), position=position_list, idf = float(doc_info[3]), metatag=float(doc_info[4]))
                if doc_id in index:
                    index[doc_id].update({term: doc_stats})
                else:
                    index[doc_id] = {term: doc_stats}
    # Initialize dictionary containing document and their score 
    # this format to update after each rank system
    doc_score = {doc_id: 0 for doc_id in index}
    cosine_scores = cosine(index, inverted_index, term_input)
    for doc_id, score in cosine_scores:
        doc_score[doc_id] += score * 1
    tf_idf_sum = tf_idf_scoring(index, term_input)
    for doc_id, score in tf_idf_sum:
        doc_score[doc_id] += score * 1
    ranked_urls = [loaded_bookmarks.find_query(k) for k, v in sorted(doc_score.items(), key=lambda item: item[1], reverse=True)]
    return ranked_urls

if __name__ == "__main__":
    search_index("software")