import json
import mongodb
from pathlib import Path

DATASAVE = "mongodb+srv://proj3Cluster:idepZy2mBvChOvan@projectcluster.5idbqzt.mongodb.net/"
DATASAVE_TWO = "mongodb+srv://jasonhw3:EBl154EMmvjllXLL@cluster0.tgq8vgu.mongodb.net/?retryWrites=true&w=majority"
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


def search_index(term_input: str):
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

    print(f"Searching for {term_input}...")
    loaded_bookmarks = LoadBookMark()
    res = query_result.split(" | ")
    list_of_document_id = [ i[:i.find(":")] for i in res]
    for id in list_of_document_id:
        print(f"{loaded_bookmarks.find_query(id)}")

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
        

if __name__ == "__main__":
    search_index("software")