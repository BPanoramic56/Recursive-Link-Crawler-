import TrieCrawler

ROOT_HTML   = "https://bpanoramic56.github.io/Panoramic56/"
TITLE       = ROOT_HTML[ROOT_HTML.rindex('/')+1:]

# websites        = 0
# success         = 0
# insiders        = 0

tree = TrieCrawler.TrieCrawler(ROOT_HTML, TITLE)
tree.initiate_crawl()

# print(tree.size())
tree.traverse()

# print(f"In {time()-start}s, {websites} were scrapped and {success} were accessible ({success/websites * 100}%)\n {insiders} insiders were found")