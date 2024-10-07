import TrieCrawler

ROOT_HTML_PANORAMIC = "https://bpanoramic56.github.io/Panoramic56/"
ROOT_HTML_CS        = "https://en.wikipedia.org/wiki/Computer_science"
ROOT_IBM            = "https://www.ibm.com/us-en"
ROOT_UTAH           = "https://www.utah.edu"
ROOT_SNOWBIRD       = "https://www.snowbird.com"
ROOT_HTML           = ROOT_HTML_PANORAMIC

TITLE       = ROOT_HTML[ROOT_HTML.rindex('/')+1:]

tree = TrieCrawler.TrieCrawler(ROOT_HTML)
tree.initiate_crawl()
tree.traverse()
tree.create_dot_graph("output.txt")