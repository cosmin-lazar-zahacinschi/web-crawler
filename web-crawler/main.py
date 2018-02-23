#!/usr/bin/env python3

from utils import logging, configuration
from crawl import crawler
from graph import G

log = logging.getLogger('root')

if __name__ == '__main__':
    
    G.start()
    
    crawler.start_crawl("http://www.hotnews.ro")
else:
    print(configuration.get_prop('prop1'))