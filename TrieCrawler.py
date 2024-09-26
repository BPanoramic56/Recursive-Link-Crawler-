import Node

import requests
from bs4 import BeautifulSoup, SoupStrainer
from time import sleep, time

class TrieCrawler:
    root_node       = None
    root_html       = None
    all_links       = set()

    def __init__(self, html, title):
        self.root_node = Node.Node(html, title)
        self.root_html = html

    def initiate_crawl(self):
        self.root_node.run(self)

    def size(self):
        return len(self.all_links)

    def traverse(self):
        self.root_node.traverseTrie()

    def check_node_existence(self, html):
        # print(f"CHECKING: {html} - {html in self.all_links}")
        return html in self.all_links

    def add_link(self, html):
        # print(f"ADDING: {html}")
        self.all_links.add(html)