import mongodb

if __name__ == "__main__":
    mongodbInstance = mongodb.DataSave("mongodb+srv://proj3Cluster:idepZy2mBvChOvan@projectcluster.5idbqzt.mongodb.net/", "Database", "Collection")

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

            