from collections import namedtuple
import json
import mongodb
from pathlib import Path
import numpy as np
import re
from bs4 import BeautifulSoup
from tokenizer import lemmatize_text
DATASAVE = "mongodb+srv://proj3Cluster:idepZy2mBvChOvan@projectcluster.5idbqzt.mongodb.net/"
DATASAVE_TWO = "mongodb+srv://jasonhw3:EBl154EMmvjllXLL@cluster0.tgq8vgu.mongodb.net/?retryWrites=true&w=majority"
TWO_GRAM_SAVE = "mongodb+srv://jasonhw3:xw24GXGcWhyi31Ly@cluster0.57kbxtr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
TWO_GRAM_SAVE_TWO = "mongodb+srv://jasonhw3:llZUsmhqHCeNNCwl@cluster0.tulx44z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE = "Database"
COLLECTION = "Collection"
BOOKKEEPER_PATH = Path("WEBPAGES_RAW") / Path("bookkeeping.json")
PAGERANK_PATH = Path('pagerank.json')
CORPUS_SIZE = 37424
Stats = namedtuple('Stats', 'count, position, tf_idf, metatag')

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

class PageRank:

    def __init__(self):
        self.jsonResult = None
        self.load_page_rank_json()
    
    def load_page_rank_json(self):
        if self.jsonResult == None:
            with open(PAGERANK_PATH, "r", encoding="utf-8") as file:
                self.jsonResult = json.loads(file.read())

    def find_page_rank(self, id_input:str):
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


def search_index(term_input: str, n_gram: int) -> str:
    """
    Loads the specific queried Index and prints the links out
    """

    if n_gram == 2:
        mongodbInstance = mongodb.DataSave(TWO_GRAM_SAVE, DATABASE, COLLECTION)
        mongodbInstance_two = mongodb.DataSave(TWO_GRAM_SAVE_TWO, DATABASE, COLLECTION)
    else:
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

    return query_result
    
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

def cosine(index: dict, inverted_index: dict, term_query: str) -> list[tuple]:
    """
    returns the cosine similarity score of each doc based on the idf of the query and 
    the doc's tf_idf score
    """
    term_idf = {}

    # -------- calculating idf for each query term ---------
    # get tf for each term in query, store in term_idf, to be replaced
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
    
    # ------------ doing cosine similarity w normalized doc vector of tf_idf scores -----
    # get score for each doc
    scores = []
    for doc_id in index.keys():
        doc_vector = np.empty(len(term_idf.keys())) # initializes np array
        for score_index, term in enumerate(term_query):
            if term in index[doc_id]:
                # if the term is in the document, add the term tf_idf to the score vector
                doc_vector[score_index] = index[doc_id][term].tf_idf
    
        # normalize doc vector
        doc_vector = doc_vector / np.linalg.norm(doc_vector)

        # get dot product of query vector and doc vector
        doc_score = np.dot(query_vector, doc_vector)
        scores.append([doc_id, doc_score])

    # sort by scores in descending order (highest score first)
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return sorted_scores

def tf_idf_scoring(index: dict, inverted_index: dict, term_query: list)-> list[tuple]:
    """
    returns the sorted normalized tf_idf scores of each doc given the users query
    """
    # get tf, store in term_idf, to be replaced
    # get sum tf-idf score for each doc
    scores = []

    # ----- making list of sum tf-idf for each doc-----
    tf_idf_list = np.empty(len(index))
    for count, doc_id in enumerate(index.keys()):
        total = 0
        for term in term_query:
            if term in index[doc_id]:
                total += index[doc_id][term].tf_idf
        scores.append([doc_id, total])
        tf_idf_list[count] = total

    # --------- normalize tf-idf of each doc ---------
    norm_factor = np.linalg.norm(tf_idf_list)
    for i in range(len(scores)):
        # normalize each doc's sum of tf_idf
        scores[i][1] = scores[i][1] / norm_factor
    
    # sort by scores in descending order (highest score first)
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return sorted_scores

def meta_scoring(index: dict, inverted_index: dict, term_query: list)-> list[tuple]:
    """
    returns the sorted normalized metatag scores of each doc given the users query
    """
    # get sum meta_tag scoring for each doc
    scores = []

    # ------- getting doc's idf metatag score -------
    meta_score_list = np.empty(len(index)) # initalize np array
    for count, doc_id in enumerate(index.keys()):
        total = 0
        for term in term_query:
            if term in index[doc_id]:
                # add term's metatag score to total score
                total += index[doc_id][term].metatag
        scores.append([doc_id, total])
        meta_score_list[count] = total

    # normalize doc's metatag idf score
    norm_factor = np.linalg.norm(meta_score_list)
    for i in range(len(scores)):
        scores[i][1] = scores[i][1] / norm_factor
    
    # sort by scores in descending order (highest score first)
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return sorted_scores

def word_proximity(index: dict, inverted_index: dict, term_query: list)-> list[tuple]:
    """
    Scores using word proximity. WIll not work with only a single query
    """
    # get sum meta_tag scoring for each doc
    scores = []
    score_list = np.empty(len(index))

    for count, doc_id in enumerate(index.keys()):
        skip = False
        word_positions = []
        for term in term_query:
            if term in index[doc_id]:
                word_positions.append(index[doc_id][term].position)
            else:
                scores.append([doc_id, 0])
                score_list[count] = 0
                skip = True
                continue
        if skip:
            continue
        min_dist = None
        continue_loop = True
        while continue_loop:
            positions = []
            for x in word_positions:
                positions.append(x[0])
            dist = max(positions) - min(positions)
            # update the min distance if the current distance is less
            if min_dist is None or dist < min_dist:
                min_dist = dist
            for x in word_positions:
                # if the first position in the list of positions is the min, remove it
                if x[0] == min(positions):
                    x.pop(0)
                    # if there are no more occurences of the term, stop the while loop
                    if len(x) == 0:
                        continue_loop = False
                    # stop for loop
                    break

        # add the score of the word proximity
        scores.append([doc_id, 1/min_dist])
        score_list[count] = 1/min_dist
    
    # normalize tf-idf
    norm_factor = np.linalg.norm(score_list)
    for i in range(len(scores)):
        scores[i][1] = scores[i][1] / norm_factor
    
    # sort by scores in descending order (highest score first)
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return sorted_scores


def query(term_input: str) -> list[str]:
    """
    returns the a list of ranked urls and a list of ranked doc ids given a string input

    Structure for index
    "folder": {"term": stats, "computer": stats(count=4,position=[3],idf=.23,metatag=1)}
    inverted index is as expected
    """
    term_input = " ".join(lemmatize_text(term_input))
    loaded_bookmarks = LoadBookMark()
    loaded_pageranks = PageRank()

    term_list_one = term_input.split()
    term_list_two = []
    index_one = {}
    inverted_index_one = {}
    index_two = {}
    inverted_index_two = {}
    remove_term_one = []
    remove_term_two = []

    if len(term_list_one) > 1:
        print("entering")
        # creating bigram index and inverted index
        term_list_two = list(zip(*[term_input.split()[i:] for i in range(2)]))
        term_list_two = [(' '.join(i)).strip().lower() for i in term_list_two]
        for term in term_list_two:
        # get all of the postings associated with the term
            query_result = search_index(term, 2)
            if query_result is None:
                remove_term_one.append(term)
            else:
                # inverted
                postings = query_result.split(" | ")
                inverted_index_one[term] = postings
                for doc in postings:
                    doc_info = doc.split(":")
                    doc_id = doc_info[0]
                    position_list = doc_info[2].strip("[").strip("]").split(",")
                    position_list = [int(i) for i in position_list]
                    doc_stats = Stats(count=int(doc_info[1]), position=position_list, tf_idf = float(doc_info[3]), metatag=float(doc_info[4]))
                    if doc_id in index_one:
                        index_one[doc_id].update({term: doc_stats})
                    else:
                        index_one[doc_id] = {term: doc_stats}
        for term in remove_term_two:
            term_list_one.remove(term)

    # creating one gram index and inverted index
    for term in term_list_one:
        # get all of the postings associated with the term
        query_result = search_index(term, 1)
        if query_result is None:
            remove_term_one.append(term)
        else:
            # inverted
            postings = query_result.split(" | ")
            inverted_index_one[term] = postings
            for doc in postings:
                doc_info = doc.split(":")
                doc_id = doc_info[0]
                position_list = doc_info[2].strip("[").strip("]").split(",")
                position_list = [int(i) for i in position_list]
                doc_stats = Stats(count=int(doc_info[1]), position=position_list, tf_idf = float(doc_info[3]), metatag=float(doc_info[4]))
                if doc_id in index_one:
                    index_one[doc_id].update({term: doc_stats})
                else:
                    index_one[doc_id] = {term: doc_stats}
    for term in remove_term_one:
        term_list_one.remove(term)
    
    # (function, weight, query size requirement)
    scoring_functions = [
        (cosine, 1, 1),
        (tf_idf_scoring, 1, 1),
        (meta_scoring, 1, 1),
        (word_proximity, 1, 2)
    ]

    # Initialize dictionary containing document and their score
    # this format to update after each rank system
    doc_score_one = {doc_id: 0 for doc_id in index_one}
    doc_score_two = {}


    # calculate each of the functions and add their scores together with respect to
    # their associated weight
    for func, weight, query_size_requirement in scoring_functions:
        if len(term_list_one) >= query_size_requirement:
            scores = func(index_one, inverted_index_one, term_list_one)
            for doc_id, value in scores:
                doc_score_one[doc_id] += value * weight
    
    #  now do it for bigrams if the query is long enough
    if len(index_two) != 0:
        doc_score_two = {doc_id: 0 for doc_id in index_two}

        # calculate each of the functions and add their scores together with respect to
        # their associated weight
        for func, weight, query_size_requirement in scoring_functions:
            scores = func(index_two, inverted_index_two, term_list_two)
            for doc_id, value in scores:
                doc_score_two[doc_id] += value * weight
    
    # combine both doc scores
    combined_doc_score = doc_score_one
    if len(doc_score_two) != 0:
        for key in combined_doc_score.keys():
            doc2_score = doc_score_two.get(key, None)
            if doc2_score is not None:
                # add doc 2 score and page rank
                combined_doc_score[key] += 0.5 * doc2_score
                combined_doc_score[key] += loaded_pageranks.find_page_rank(key) / 3
            else:
                # add page rank
                combined_doc_score[key] = doc2_score
                combined_doc_score[key] += loaded_pageranks.find_page_rank(key) / 3


    ranked_urls = [loaded_bookmarks.find_query(k) for k, v in sorted(combined_doc_score.items(), key=lambda item: item[1], reverse=True)]
    ranked_doc_ids = [k[0] for k in sorted(combined_doc_score.items(), key=lambda item: item[1], reverse=True)]
    return ranked_urls, ranked_doc_ids

def get_query_details(doc_id: str) -> dict:
    """
    returns the text inside the html tag for title given the doc id
    - used for gui
    """
    folder = doc_id[:doc_id.find("/")]
    file = doc_id[doc_id.find("/") + 1:]

    with open(Path("WEBPAGES_RAW") / folder / file, encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else "Unknown Title"
                    
    return title


def get_html_info(doc_id: str) -> str:
    """
    returns all the html in a doc given the doc id
    """
    folder = doc_id[:doc_id.find("/")]
    file = doc_id[doc_id.find("/") + 1:]

    with open(Path("WEBPAGES_RAW") / folder / file, encoding='utf-8') as file:
        file_results = file.read()
    
    return file_results


# if __name__ == "__main__":
#     test_result = search_index("uci")
#     print(test_result)