# https://github.com/iaorana/swap-exposer

import sys
import re
import urllib2
from bs4 import BeautifulSoup
from urlparse import urlparse
import ssl

def main(argv):
    domain = str(sys.argv[1])
    archive_url = 'https://web.archive.org/web/*/http://%s/*' % domain
    context = ssl._create_unverified_context()

    # first capture the results from the search query
    response = getResults(domain, archive_url)
    # now lets parse the page for links
    parsedsoup = parseHTML(response)
    # next we will cut down the list of links to what we care about
    hits = parseLinks(parsedsoup)

    printurls(hits)
    headrequests(hits, context)

    print('Operation completed.')

def headrequests(hits, context):
    print('HEAD requests.')
    for line in hits:
        match_swap = re.search('.swp$', urlparse(line).path)
        if match_swap:
            result = processhead(line, context)
        else:
            line = line + '.swp'
            result = processhead(line, context)
        if result is None:
            continue
        if result.getcode() is 200:
            # this tests to see if the webserver is catching all requests
            catchall_result = processhead(line + '.asdasdasdasdasd', context)
            if catchall_result is None:
                print (line + ' found.')
            else:
                print(line + ' catchall detected.')

def processhead(line, context):
    request = urllib2.Request(line)
    request.get_method = lambda: 'HEAD'
    try:
        response_head = urllib2.urlopen(request, context=context)
    except urllib2.HTTPError:
        return None
    return response_head

def printurls(hits):
    for line in hits:
        print(line)
    print(str(len(hits)) + ' unique files found.')

def getResults(domain, archive_url):
    opener = urllib2.build_opener()
    print('Search query requested for %s.' % domain)
    response = opener.open(archive_url)
    print('Search response received.')
    return response

def parseHTML(response):
    print('Parsing HTML.')
    soup = BeautifulSoup(response, 'html.parser')
    return soup

def parseLinks(soup):
    print('Parsing links.')
    hits = set()
    for link in soup.find_all('a'):
        urllink = (link.get('href'))
        # remove the archive.org links from the page
        if (urlparse(urllink).path == '/index.jsp'):
            urllink = 'skip'
        match_archive = re.search('archive.org', urlparse(urllink).netloc)
        if match_archive:
            continue
        else:
            urllink = reduceLinks(urllink)
            if urllink is not None:
                hits.add(urllink)
    return hits

def reduceLinks(urllink):
    match_ext = re.search('(\.php|\.jsp|\.cfm|\.cfml|\.asp|\.phpx|\.swp|\.save|\~$)', urllink)
    if match_ext:
        # this will strip off the /web/*/ from the URLs and get us back to the direct URL
        p = re.compile('^(.+)/http')
        return p.sub('http', urlparse(urllink).path)

if __name__ == '__main__':
    main(sys.argv)
