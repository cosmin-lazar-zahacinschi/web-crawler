from urllib.request import Request, urlopen
from crawl import log
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, urlunsplit, quote, quote_plus
from graph import G

def sanitize_url(url):

    scheme, netloc, path, qs, anchor = urlsplit(url)
    path = quote(path, '/%')
    qs = quote_plus(qs, ':&=')
    return urlunsplit((scheme, netloc, path, qs, anchor))

def parse_url(current_url, to_visit_set):
    # create the request
    log.info('Opening ' + current_url)
    
    try:
        req = Request(current_url, headers={'User-Agent':'Mozilla/5.0'})
        resp = urlopen(req)
    except IOError as e:
        log.error(e)
        return
    except UnicodeError as e:
        log.error(e)
        return
    
    # parse only html's for now
    if not 'text/html' in resp.headers['Content-Type']:
        return
    
    soup = BeautifulSoup(resp, 'html.parser')
    links = soup.find_all('a')
    
    current_split = urlsplit(current_url)
    
    for link in links:
        next_url = ''
        next_split = urlsplit(link.get('href'))
        
        scheme = next_split.scheme if next_split.scheme != '' else current_split.scheme
        if (scheme == 'http' or scheme == 'https'):
            next_url += scheme + '://'
        else:
            # no scheme, jump to next url
            continue
        
        netloc = next_split.netloc if next_split.netloc != '' else current_split.netloc
        if (netloc != ''):
            next_url += netloc
        else:
            # no netcol, jump to next url
            continue
        
        path = next_split.path if next_split.path != '' else current_split.path
        if (path != ''):
            next_url += path
        
        query = next_split.query if next_split.query != '' else current_split.query
        if (query != ''):
            next_url += '?' + query
        
        sanitized = sanitize_url(next_url)
        if not sanitized in to_visit_set:
            to_visit_set.add(sanitize_url(next_url))
            if (current_split.netloc != next_split.netloc):
                G.add_connection(current_split.netloc, next_split.netloc)
        
    resp.close()
    
def start_crawl(url):
    
    # initialize set with the received url
    to_visit_set = {url}
    
    while len(to_visit_set) > 0:
        popped_url = to_visit_set.pop()
        parse_url(popped_url, to_visit_set)
    
    