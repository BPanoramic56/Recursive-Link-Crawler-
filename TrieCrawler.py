import Node

import requests
from bs4 import BeautifulSoup, SoupStrainer
from time import sleep, time
from os import remove

class TrieCrawler:
    root_node       = None
    root_html       = None
    all_links       = set()
    errors          = 0

    def __init__(self, html):
        self.root_node = Node.Node(html)
        self.root_html = html

    def initiate_crawl(self):
        self.root_node.run(self)

    def size(self):
        return len(self.all_links)

    def traverse(self):
        self.root_node.traverseTrie()

    def check_node_existence(self, html):
        return html in self.all_links
    
    def get_specific_node(self, html):
        visited = set()
        return self.root_node.find(html, visited)

    def add_link(self, html):
        self.all_links.add(html)
        print(self.size(), end="\r")
        
    def error_opening_website(self, error, html):
        self.errors += 1
    
    def add_cycle(self, callingNode, html):
        cyclic_node = self.get_specific_node(html)
        if cyclic_node:  # Check if node was found before calling add_cycle
            cyclic_node.add_cycle(callingNode)
    
    def create_dot_graph(self, filename):
        self.initial_dot_setup(filename)
        self.cleanse_file(filename)
        remove("temp_file.txt")
        
    def initial_dot_setup(self, filename):
        self.empty_text_file("temp_file.txt")
        self.empty_text_file(filename)
        
        file = open("temp_file.txt", "a")
        file.write("Digraph " + self.root_node.title + "{\n")
        self.root_node.create_graph(file)
        file.write("}")
        file.close()

    def cleanse_file(self, filename):
        lines_seen = set()

        with open(filename, 'a') as out_file:
            with open("temp_file.txt", 'r') as in_file:
                for line in in_file:
                    if line not in lines_seen:
                        out_file.write(line)
                        lines_seen.add(line)


    def empty_text_file(self, filename):
        file = open(filename, "w")
        file.write("") # Cleaning the file
        file.close()