import json

def get_dict_from_json():
    """
    turns the corpus.json into a dict
    """
    with open("corpus.json", "r", encoding="utf-8") as corpus:
        jsonResult = json.loads(corpus.read())
    return jsonResult


def get_num_unique_words(corpus: dict):
    """
    returns the number of unique words in the index
    """
    return len(corpus)

def get_num_unique_doc_ids(corpus: dict):
    doc_ids = set()
    for val in corpus.values():
        list_docs = val.split(' | ')
        for doc in list_docs:
            doc_id = doc.split(':')[0]
            doc_ids.add(doc_id)
    return len(doc_ids)

if __name__ == "__main__":
    corpus = get_dict_from_json()
    num_unique_words = get_num_unique_words(corpus)
    num_unique_docs = get_num_unique_doc_ids(corpus)
    print(f'Number of unique words: {num_unique_words}')
    print(f'Number of unique doc ids: {num_unique_docs}')