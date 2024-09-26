import requests
from bs4 import BeautifulSoup, SoupStrainer
from time import sleep, time

class Node:
    html            = None
    title           = None
    isCycle         = False
    branchList      = list()
    LINKS           = SoupStrainer('a')

    def __init__(self, htmlInit, titleInit=""):
        self.html       = htmlInit
        self.title      = titleInit
        
    def addChildLink(self, newNode):
        self.branchList.append(newNode)
    
    def isPartOfCycle(self):
        self.isCycle = True
    
    def getHTML(self):
        return self.html
    
    def getBranches(self):
        return self.branchList
    
    def run(self, trie):
        if not self.try_url(self.html):
            return
        
        currentRequest = requests.get(self.html)

        soup = BeautifulSoup(currentRequest.text, 'html.parser')

        for link in soup.find_all('a'):
            href = link['href']
            new_node = Node(href)

            # print(f"CURRENT: {href}")
            if trie.check_node_existence(href):
                continue
            # print(f"CURRENT 1: {href}")
            print(f"{href} - {self.html}")
            if href == self.html:
                continue

            trie.add_link(href)
            self.branchList.append(new_node)

        for node in self.branchList:
            node.run(trie)
        
    def try_url(self, html):
        try:
            request_check = requests.head(html, timeout=30)

            if not request_check.ok:
                print(f"Root HTML could not be accessed\n{request_check.status_code}")
                return False

            return True
        
        except:
            return False
    
    def traverseTrie(self):
        for node in self.branchList:
            node.traverse_trie_recursive(1)

    def traverse_trie_recursive(self, indent=0):
        if self.isCycle:
            # print(f"{'-' * indent}{self.html} (Cycle detected)")
            return

        print(f"{'- ' * indent}{self.html}")
        indent += 1

        # Set this node as part of a cycle to prevent future recursion
        self.isCycle = True

        for node in self.branchList:
            print(node.html)
            node.traverse_trie_recursive(indent)