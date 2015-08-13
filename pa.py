# -基于python的广度优先爬虫
import sys
from functools import partial
from operator import mul
import urllib2
import HTMLParser
from BeautifulSoup import BeautifulSoup
import os
import networkx as nx

# Try http://ajaxian.com/
print syspath
#URL = 'http://www.imdb.com/title/tt0108778/'
#ROOT_URL = sys.argv[1]
ROOT_URL = 'http://ajaxian.com/'
if len(sys.argv) > 2:
    MAX_DEPTH = int(sys.argv[2])
else:
    MAX_DEPTH = 1
URL = 'http://www.imdb.com/title/tt0108778/'
XFN_TAGS = set(['coggague', 'sweetheart', 'parent', 'co-worker', 'muse', 'neighbor', 'sibling', 'kin', 'child', 'me', 'acquaintance', 'met', 'crush', 'contact', 'friend'])
OUT = 'graph.dot'
depth = 0
g = nx.DiGraph()
next_queue = [ROOT_URL]
while depth < MAX_DEPTH:
    depth+=1
    (queue, next_queue) = (next_queue, [])
    for item in queue:
        try:
            page = urllib2.urlopen(item)
        except urllib2.URLError:
            print 'Failed to fetch' + item
            continue
        try:
            soup = BeautifulSoup(page)
        except HTMLParser.HTMLParseError:
            print 'Fail to parse' + item
            continue
    anchorTags = soup.findAll('a')
    if not g.has_node(item):
        g.add_node(item)
    for a in anchorTags:
        if a.has_key('rel'):
            if len(set(a['rel'].split())&XFN_TAGS)>0:
                friend_url = a['href']
                g.add_edge(item,friend_url)
                g[item][friend_url]['label'] = a['rel'].encode('utf-8')
                g.node[friend_url]['label'] = a.contents[0].encode('utf-8')
                next_queue.append(friend_url)
                tags = a['rel'].split()
                print a.contents[0], a['href'],tags

if not os.path.isdir('out'):
    os.mkdir('out')
try:
    nx.drawing.write_dot(g,os.path.join('out', OUT))
except ImportError, e:
    dot = []
    for (n1, n2) in g.edges():
        dot.append('"%s" [label="%s"]' % (n2, g.node[n2]['label']))
        dot.append('"%s" -> "%s" [label="%s"]' % (n1, n2, g[n1][n2]['label']))
f = open(os.path.join('out', OUT),'w')
f.write('''strict digarph{
%s
}''' %(';\n'.join(dot),))
f.close()

