from utils import logging
from crawl import crawler
from graph import G

log = logging.getLogger('root')

if __name__ == '__main__':
    
    G.start()
    
    crawler.start_crawl("http://www.hotnews.ro")