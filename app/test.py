import json
import urllib2
from pprint import pprint
import rdflib
import conceptnet5
from conceptnet5.query import lookup
import wikipedia
from textblob import TextBlob
from nltk.corpus import stopwords
from practnlptools.tools import Annotator
import re
from SPARQLWrapper import SPARQLWrapper, JSON
import WordNet


from nltk.corpus import wordnet as wn

#acknowledgment_synset = wn.synset('repeat.v.01').lemmas
#acknowledgment_lemma = acknowledgment_synset.lemmas[0]
#print  wn.lemma('bright.a.01.bright').derivationally_related_forms()

#print(acknowledgment_lemma.derivationally_related_forms())


#test = json.load(urllib2.urlopen("http://www.freesound.org/apiv2/search/text/?query=dogs&token=06mS7W2OiXidVC2tQ4ikMfe3nomU7rBptaJgBCvp"))
#test2 = json.load(urllib2.urlopen("https://api.jamendo.com/v3.0/artists/?client_id=4cb8fab9&format=jsonpretty&name=we+are+fm"))

#pprint(test2)
#g = rdflib.Graph()
#mo = g.parse("http://purl.org/ontology/mo/")
#print("graph has %s statements." % len(mo))
#for stmt in mo:
    #pprint(stmt)

#for subj, pred, obj in mo:
   #pprint(subj +" ///// "+ obj)

#for subj, pred, obj in mo:
    #moSub = subj


#for assertion in lookup('/c/en/example'):
    #print(assertion)
#annotator = Annotator()
#term= TextBlob("Articles including recorded pronunciations (UK English).")
#filtered_words = [w for w in term.words if not w in stopwords.words('english')]
#print filtered_words
#el = wikipedia.page("Night")
#print wikipedia.summary(el)
#print(el.content)
searchFor="London"


print wikipedia.search(searchFor)
wiki = TextBlob(wikipedia.summary(searchFor, sentences=1))
#wikiSum = TextBlob(wikipedia.summary(searchFor))
print wiki
#print wikiSum

filtered_words = [w for w in wiki.words if not w in stopwords.words('english')]
#print filtered_words

#annotator.getAnnotations(wikipedia.summary("London", sentences=1))['chunk']

#word = wn.synset(searchFor+'.n.01')
#print word.hypernyms()

annotator = Annotator()
result = re.sub('\(.*?\)',"", wiki.string)
result = re.sub("\/.+?\/","", result)
#print result
dep_parse = annotator.getAnnotations(result, dep_parse=True)['dep_parse']
dp_list = dep_parse.split('\n')
#print dp_list

spotlightTerms = WordNet.spotlightSearch("London is the capital and most populous city of England and the United Kingdom.")
print dp_list


def dpbediaQuery(query):
    #test = json.load(urllib2.urlopen("http://www.freesound.org/apiv2/search/text/?query=" + term + "&token=06mS7W2OiXidVC2tQ4ikMfe3nomU7rBptaJgBCvp"))
    #test2 = json.load(urllib2.urlopen("https://api.jamendo.com/v3.0/tracks/?client_id=4cb8fab9&format=jsonpretty&name=" + term))
    #pprint(test)
    #pprint(test2)
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
        PREFIX dbres: <http://dbpedia.org/resource/>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT  ?category
        WHERE {  <http://dbpedia.org/resource/Category:"""+query+""">  skos:broader ?category.}
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    #pprint (results)

    for result in results["results"]["bindings"]:
        resource=str(result["category"]["value"]).replace("http://dbpedia.org/resource/Category:","").replace("_"," ")
        print(resource)
        categoryElements = TextBlob(resource)
        print (categoryElements.pos_tags)
dpbediaQuery("London")


#print(wn.synsets('port'))
wupalmerMAX=0
for synset in wn.synsets('port', pos=wn.NOUN):
    synset=str(synset).replace("Synset('","").replace("')","")
    print "-------------------------------------"
    print synset, wn.synset(synset).definition()
    for synset2 in wn.synsets('capital', pos=wn.NOUN):
        synset2 = str(synset2).replace("Synset('", "").replace("')", "")
        lch = wn.synset(synset).lowest_common_hypernyms(wn.synset(synset2))
        wupalmer=wn.wup_similarity(wn.synset(synset),wn.synset(synset2))
        #print synset2, wn.synset(synset2).definition()
        #print lch
        #print wupalmer
        if wupalmerMAX<wupalmer:
            print lch
            wupalmerMAX=wupalmer
            print "Max is: " + str(wupalmerMAX), str(synset), str(wn.synset(synset).definition()) + "/" + str(synset2), str(wn.synset(synset2).definition())
        print "--------------------------------------"



