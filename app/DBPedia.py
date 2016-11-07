from SPARQLWrapper import SPARQLWrapper, JSON
import urbandictionary as ud
from PyDictionary import PyDictionary
import urllib2, json
from pprint import pprint
from nltk.corpus import wordnet as wn

def dpbediaQuery(query):

    if str(query[0]) == 'of':
        results = dpbediaQueryTypeOF(query)
    if str(query[0]) == 'at':
        results = dpbediaQueryTypeAT(query)
    if str(query[0]) == 'like':
        results = dpbediaQueryTypeLIKE(query)

    return results




def dpbediaQueryTypeOF(query):
    term = query[1]
    # test = json.load(urllib2.urlopen("http://www.freesound.org/apiv2/search/text/?query=" + term + "&token=06mS7W2OiXidVC2tQ4ikMfe3nomU7rBptaJgBCvp"))
    # test2 = json.load(urllib2.urlopen("https://api.jamendo.com/v3.0/tracks/?client_id=4cb8fab9&format=jsonpretty&name=" + term))
    # pprint(test)
    # pprint(test2)
    dictionary = PyDictionary()
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX dcterms: <http://purl.org/dc/terms/>
            SELECT ?subject
            WHERE { <http://dbpedia.org/resource/""" + term + """> dcterms:subject ?subject }
        """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print results
    for result in results["results"]["bindings"]:
        print "++++++++++++++++++++++++++++++++++++"
        print(result["subject"]["value"])
        print "++++++++++++++++++++++++++++++++++++"
        sparql.setQuery("""
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dcterms: <http://purl.org/dc/terms/>
                SELECT ?subject ?label
                WHERE { ?subject dcterms:subject <""" + result["subject"]["value"] + """>.}
                LIMIT 3
                """)
        sparql.setReturnFormat(JSON)
        results2 = sparql.query().convert()
        for result2 in results2["results"]["bindings"]:
            print(result2["subject"]["value"].replace("http://dbpedia.org/resource/", ""))
            expandedTerm = result2["subject"]["value"].replace("http://dbpedia.org/resource/", "")
            # test = json.load(urllib2.urlopen("http://www.freesound.org/apiv2/search/text/?query=" + expandedTerm + "&token=06mS7W2OiXidVC2tQ4ikMfe3nomU7rBptaJgBCvp"))
            # pprint (test)
    return results

def dpbediaQueryTypeAT(query):
    print 'Query type AT'
    term = query[1]
    # test = json.load(urllib2.urlopen("http://www.freesound.org/apiv2/search/text/?query=" + term + "&token=06mS7W2OiXidVC2tQ4ikMfe3nomU7rBptaJgBCvp"))
    # test2 = json.load(urllib2.urlopen("https://api.jamendo.com/v3.0/tracks/?client_id=4cb8fab9&format=jsonpretty&name=" + term))
    # pprint(test)
    # pprint(test2)
    dictionary = PyDictionary()
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dcterms: <http://purl.org/dc/terms/>
                SELECT ?subject
                WHERE { <http://dbpedia.org/resource/""" + term + """> dcterms:subject ?subject }
            """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print results
    return results

def dpbediaQueryTypeLIKE(query):
    term = query[1]
    synonyms=[]
    print 'Query type LIKE'
    for ss in wn.synsets(term):
        print(ss)
        for sim in ss.similar_tos():
            print('    {}'.format(sim))
    return str(wn.synsets(term))

def dpbediaQueryTypeFOR(query):
    print 'Query type FOR'
    #return results

def dpbediaQueryTypeFROM(query):
    print 'Query type FROM'
    #return results

def dpbediaQueryTypeBEFORE(query):
    print 'Query type BEFORE'
    #return results

def dpbediaQueryTypeIN(query):
    print 'Query type IN'
    #return results


