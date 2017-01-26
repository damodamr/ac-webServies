import urllib2
import nltk
from bs4 import BeautifulSoup, Tag
from textblob import TextBlob, Word
from textblob.np_extractors import ConllExtractor, FastNPExtractor
from practnlptools.tools import Annotator
from nltk.corpus import wordnet as wn
import CreateGraphNeo4J
from nltk.corpus import propbank
import wikipedia
import WordNet

annotator=Annotator()
#extractor = ConllExtractor()
extractor = FastNPExtractor()

DOWNLOAD_URL = 'http://www.nhs.uk/conditions/'

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
req = urllib2.Request(DOWNLOAD_URL, headers=hdr)

try:
    page = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.fp.read()

content = page.read()

soup = BeautifulSoup(content)
for tag in soup.find_all('strong'):
    tag.replaceWith('')

text = soup.get_text()

zen = TextBlob(text)

sentences = zen.sentences

#print sentences
#print soup.prettify()
print soup.title
for link in soup.find_all('a'):
    print(link.get('href'))
    links = link.get('href')
    print "http://www.nhs.uk" + link.get('href')






