import json
import mongodb
from pathlib import Path

DATASAVE = "mongodb+srv://proj3Cluster:idepZy2mBvChOvan@projectcluster.5idbqzt.mongodb.net/"
DATABASE = "Database"
COLLECTION = "Collection"
BOOKKEEPER_PATH = Path("WEBPAGES_RAW") / Path("bookkeeping.json")


class LoadBookMark:
    
    def __init__(self):
        self.jsonResult = None
        self.load_bookmark_json()
    
    def load_bookmark_json(self):
        if self.jsonResult == None:
            with open(BOOKKEEPER_PATH, "r", encoding="utf-8") as bookkeeper_file:
                self.jsonResult = json.loads(bookkeeper_file.read())
    
    def find_query(self, id_input:str):
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

def search_index(term_input: str):
    """
    Loads the specific queried Index and prints the links out
    """
    mongodbInstance = mongodb.DataSave(DATASAVE, DATABASE, COLLECTION)
    query_result = mongodbInstance.get_query(term_input)[term_input]
    loaded_bookmarks = LoadBookMark()
    string_term = ""
    list_of_document_id = []
    res = query_result.split(" | ")
    for i in res:
        string_term += i[:i.find(":")] + " "
        list_of_document_id.append(i[:i.find(":")])
    for id in list_of_document_id:
        print(f"{loaded_bookmarks.find_query(id)} | ({id})")

def all_terms():
    """
    All terms stored in the database
    """
    mongodbInstance = mongodb.DataSave(DATASAVE, DATABASE, COLLECTION)
    list_of_terms = []
    for document in mongodbInstance.retreive_all_data():
        # Remove the '_id' field from the document
        del document['_id']
        # Iterate over key-value pairs in the document
        for term in document.keys():
            list_of_terms.append(term)
    
    print(list_of_terms)
        

if __name__ == "__main__":
    search_index("software")