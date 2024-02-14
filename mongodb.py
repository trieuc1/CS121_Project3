import pymongo


class DataSave:

    def __init__(self, client, database, collection):
        """
        client -> mongodb link
        database -> database of the client
        collection -> collection of the database
        """
        self.client = client
        self.database = database
        self.collection = collection
        print(f"[MongoDB Manager] Setup")
    
    def __get_collection(self):
        """
        Gets the collection of the MongoDB database
        """
        client = pymongo.MongoClient(self.client)
        clientDatabase = client[self.database]
        clientCollection = clientDatabase[self.collection]
        return client, clientCollection
        
    
    def save_data(self, query_save: dict):
        """
        Use .json format to save data
        """
        client, clientCollection = self.__get_collection()
        result = clientCollection.insert_one(query_save)
        print(f"[MongoDB Manager] Saved Data: {query_save} | {result}")
        client.close()
    
    def retreive_all_data(self):
        """
        Returns All of the Data in the Database
        """
        client, clientCollection = self.__get_collection()
        all_data = clientCollection.find()
        dict_data = [data for data in all_data]
        client.close()
        print(f"[MongoDB Manager] Obtained All Data")
        return dict_data

    def update_query(self, query_input: dict, new_query_input: dict):
        """
        Updates a single element
        """
        client, clientCollection = self.__get_collection()
        update_result = clientCollection.update_one(query_input, new_query_input)
        client.close()
        print(update_result)

    def delete_query(self, query_input: dict):
        """
        Delete a Single Element
        """
        client, clientCollection = self.__get_collection()
        update_result = clientCollection.delete_one(query_input)
        client.close()
        print(update_result)

    def remove_collection(self):
        """
        Removes all of the data in the collection!
        """
        client, clientCollection = self.__get_collection()
        query_result = clientCollection.delete_many({})
        client.close()
        print(f"[MongoDB Manager] Deleted a total of {query_result.deleted_count} documents.")
    
    def get_documents(self, string_input):
        """
        Gets all of the documents given a string input
        """
        BASE_QUERY = {string_input: {"$exists": True}} 
        client, clientCollection = self.__get_collection()
        query_result = clientCollection.find_one(BASE_QUERY)
        client.close()
        print(f"[MongoDB Manager] Found Document: {query_result}")
        return query_result


if __name__ == "__main__":
    #examples of what you can do. Might have to whitelist IP Address for it to work, essentially you can store your string client, put database name and collection and it
    #should work
    CurData = DataSave("mongodb+srv://cs121:cs121@cs121rpoject3m1.1wqbe90.mongodb.net/?retryWrites=true&w=majority", "Database", "Collection")
    CurData.save_data({'docID': 1, 'terms': ["hello", "world"]})
    res = CurData.retreive_all_data()
    print(res)
    CurData.remove_collection()
    #-------------------TESTING------------------#
    print("-----------------------TESTING-------------------------")
    CurData.save_data({"Hello": [(1, 6, [1, 9, 27], 8.99, 10)]})
    CurData.save_data({"Word": [(1, 6, [1, 9, 27], 8.99, 10)]})
    CurData.save_data({"exampleToken": [(1, 6, [1, 9, 27], 8.99, 10)]})
    CurData.save_data({"tokenStorage": [(1, 6, [1, 9, 27], 8.99, 10)]})
    resultFound = CurData.get_documents("Hello")
    print(resultFound)
    res = CurData.retreive_all_data()
    CurData.remove_collection()

