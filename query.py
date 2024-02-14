import json
def load_index():
    """
    Loads the index in
    """
    with open("corpus.json", "r") as in_file:
        index_dict = json.load(in_file)
        