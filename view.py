from corpus import Corpus
from bs4 import BeautifulSoup
from pathlib import Path
if __name__ == "__main__":
    corpus_dir = Path(r"C:\Users\dnp2k\Downloads\Github\CS121_Project3\WEBPAGES_RAW")
    url = input("Enter url:")
    corpus_dir = corpus_dir / url
    print(corpus_dir)
    with open(corpus_dir, 'rb') as file:
        content = file.read()
        html = BeautifulSoup(content, 'lxml')
        print(html.get_text())