import requests
from bs4 import BeautifulSoup
from time import sleep, time
import re
import string
import resource, sys
sys.setrecursionlimit(2000)

headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}
class Node:
    def __init__(self, htmlInit):
        self.html = htmlInit
        self.title = self.generate_name()
        self.isCycle = False
        self.branchList = []
        self.cycleList = []

    def generate_name(self):
        result = self.html.rsplit('/', 1)[-1]
        if not result:
            last_slash_pos = self.html.rfind('/')
            second_last_slash_pos = self.html.rfind('/', 0, last_slash_pos)
            result = self.html[second_last_slash_pos + 1:last_slash_pos]

        translation_table = str.maketrans(string.punctuation, '_' * len(string.punctuation))
        result = result.translate(translation_table)
        return result

    def add_cycle(self, callingNode):
        self.cycleList.append(callingNode)

    def run(self, trie):
        # Stop recursion if max depth is reached

        if not self.try_url(self.html):
            return
        
        session = requests.Session()
        session.max_redirects = 20

        try:
            currentRequest = session.get(self.html)
            soup = BeautifulSoup(currentRequest.text, 'html.parser')
        except:
            return
        
        for link in soup.find_all(href=True):
            try:
                href = link['href']
            except Exception as error:
                trie.error_opening_website(error, link)
                continue

            # Normalize href to avoid crawling duplicate pages with slight variations
            href = requests.compat.urljoin(self.html, href)

            if trie.check_node_existence(href):
                trie.add_cycle(callingNode=self, html=href)
                continue

            if href == self.html:
                continue
            new_node = Node(href)

            trie.add_link(href)
            self.branchList.append(new_node)

        for node in self.branchList:
            node.run(trie)

    def traverseTrie(self):
        print(f"- {self.title}")
        for node in self.branchList:
            node.traverse_trie_recursive(2)

    def traverse_trie_recursive(self, indent=0):
        print(f"{'- ' * indent}{self.title}")

        indent += 1
        for node in self.branchList:
            node.traverse_trie_recursive(indent)
    
    def try_url(self, html):
        try:
            request_check = requests.head(html, timeout=30)
            if not request_check.ok:
                return False
            return True
        except Exception as e:
            return False
        
    # def find(self, target, visited):
        
    #     # If this node has already been visited, return None to avoid infinite recursion
    #     if self.html in visited:
    #         return None
        
    #     # Mark this node as visited
    #     visited.add(self.html)

    #     # If the current node matches the target, return this node
    #     if self.html == target:
    #         return self

    #     # Otherwise, search recursively in the child nodes
    #     for node in self.branchList:
    #         found_node = node.find(target, visited)
    #         if found_node:  # If the target was found in any child, return it
    #             return found_node
    #     return None
    def find(self, target, visited):
        # If this node has already been visited, return None to avoid infinite recursion
        if self.html in visited:
            return None
        
        # Mark this node as visited
        visited.add(self.html)

        # If the current node matches the target, return this node
        if self.html == target:
            return self

        # Otherwise, search recursively in the child nodes
        for node in self.branchList:
            found_node = node.find(target, visited)
            if found_node:  # If the target was found in any child, return it
                return found_node
        return None
    
    def create_graph(self, file):
        for Node in self.cycleList:
            file.write(f"\t{Node.title} -> {self.title}\n")

        for Node in self.branchList:
            file.write(f"\t{self.title} -> {Node.title}\n")
            Node.create_graph(file)