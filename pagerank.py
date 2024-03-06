from query import LoadBookMark
import json
import re
import numpy as np
from networkx.convert_matrix import from_numpy_array
from networkx.algorithms.link_analysis.pagerank_alg import pagerank
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse

WEBPAGES_PATH = "WEBPAGES_RAW"

def get_bookkeeper() -> dict:
    """
    gets the json_dict from the bookkeeping file
    """
    # set of bookkeeper id's w links that are unique
    bookkeeper_path = Path(WEBPAGES_PATH) / "bookkeeping.json"
    with open(bookkeeper_path, encoding='utf-8') as file:
        json_dict = json.load(file)

    return json_dict

bookmark = LoadBookMark() # used for getting base link
bookkeeper = get_bookkeeper()
doc_ids_list = list(bookkeeper.keys())

def get_page_rank_scores():
    """
    returns the page rank scores in the form of a dictionary {node: score}
    """
    adj_matrix = create_adjacency_matrix(doc_ids_list)
    with open('matrix.txt', 'w') as f:
        for line in adj_matrix:
            f.write(f"{line}\n")
    return pagerank(get_graph(adj_matrix))
    # # initialize pagerank scores w uniform scores
    # num_nodes = len(doc_ids_list)
    # page_rank_scores = np.ones(num_nodes) / num_nodes
    # for i in range(max_iterations):
    #     new_page_rank_scores = adj_matrix.dot(page_rank_scores)

    #     # add teleportation prob
    #     new_page_rank_scores = teleport_prob + (1 - teleport_prob) * new_page_rank_scores
    
    #     # check for convergence
    #     if np.allclose(page_rank_scores, new_page_rank_scores):
    #         break
    # page_rank_scores = new_page_rank_scores
    # return page_rank_scores

def get_graph(adj_matrix):
    """
    converts the adjacency matrix into a graph
    
    returns a graph
    """
    return from_numpy_array(adj_matrix)

def create_adjacency_matrix(doc_ids_list):
    """
    creates an adjacency matrix for each doc_id where an edge is whether the page links to another page

    returns the adj_matrix (np array)
    """
    n = len(doc_ids_list)
    adj_matrix = np.zeros((n, n), dtype=int)
    for i in range(len(doc_ids_list)):
        doc_id = doc_ids_list[i]
        print(doc_id)
        links = get_doc_links(doc_id)
        for link in links:
            connected_id = get_doc_id_from_link(link)
            print("connected_id", connected_id )
            if connected_id is not None:
                # directed graph
                adj_matrix[i][doc_ids_list.index(connected_id)] += 1
                adj_matrix[doc_ids_list.index(connected_id)][i] += 1
    return adj_matrix

def is_valid_href(href):
    """
    checks that its a url
    """
    # Regular expression to check if the href starts with 'http', 'https', 'ftp'
    regex = r"^(http|https|ftp)://"
    
    # Check if the href matches the regular expression
    if href is not None and re.match(regex, href):
        return True
    else:
        return False

def remove_scheme(url):
    """
    removes the scheme part of the url ex. https://
    """

    parsed_url = urlparse(url)
    scheme_removed_url = parsed_url.netloc + parsed_url.path + parsed_url.query + parsed_url.fragment
    return scheme_removed_url

def get_doc_links(doc_id):
    """
    in each document, it searches and collects all the links in it
    """
    path_string = Path(WEBPAGES_PATH) / doc_id
    with open(path_string, 'rb') as file:
        content = file.read()
        html = BeautifulSoup(content, 'lxml')
        links = [remove_scheme(a_tag.get('href')) for a_tag in html.find_all('a') if is_valid_href(a_tag.get('href')) ]
        return links

def get_doc_id_from_link(link: str):
    """
    given a link, it finds the doc_id associated if it exists
    
    else it returns None
    """
    for doc_id, value in bookkeeper.items():
        if value == link:
            return doc_id
    return None

# making the doc_ids the key and the page_rank_score its value
print("hello")
page_rank_scores = get_page_rank_scores().values()
page_rank_scores = dict(zip(doc_ids_list, page_rank_scores))

with open("pagerank.json", 'w') as file:
    json.dump(page_rank_scores, file)
print("done")