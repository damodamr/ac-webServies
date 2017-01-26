from SPARQLWrapper import SPARQLWrapper, JSON
import urbandictionary as ud
from PyDictionary import PyDictionary
import urllib2, json
from pprint import pprint
from nltk.corpus import wordnet as wn
import WordNet

def dpbediaQuery(prepType, resource):

    if str(prepType) == 'of':
        relation = ["dct:subject"]
        relation2= ["dbo:musicComposer","dbo:composer"]
        results = dpbediaQueryTypeOF(resource, relation2)
    if str(prepType) == 'at':
        relation = ["dct:subject"]
        relation2 = ["dbp:place", "dbp:knowFor", "dbp:associatedActs", "dbp:associatedBands"]
        results = dpbediaQueryTypeAT(resource, relation2)
    if str(prepType) == 'like':
        results = dpbediaQueryTypeLIKE(resource)
    if str(prepType) == 'for':
            relation = ["dbo:genre", "dbo:field"]
            results = dpbediaQueryTypeAT(resource, relation)
    if str(prepType) == 'from':
            relationPlace = ["dbp:place", "dbp:knowFor", "dbp:associatedActs", "dbp:associatedBands"]
            relationAssociation = ["dbo:musicComposer", "dbp:music"]
            results = dpbediaQueryTypeAT(resource, relationAssociation)
    if str(prepType) == 'by':
            relation = ["dbo:composerOf", "dbo:title", "dbo:soundRecording"]
            results = dpbediaQueryTypeAT(resource, relation)
    if str(prepType) == 'before' or str(prepType) == 'after':
            relation = ["dbp:date", "dbp:years", "dbo:musicalWork", "dbo:recordDate"]
            results = dpbediaQueryTypeAT(resource, relation)
    if str(prepType) == 'in':
            relation = []
            results = dpbediaQueryTypeAT(resource, relation)
    return results


#--------------------OF-------------------------------------------------------------------------------------------------

def dpbediaQueryTypeOF(resource, relations):

    dbresource =  resource
    print "dbresource is %s" %dbresource
    print "relation is %s" %relations
    # test = json.load(urllib2.urlopen("http://www.freesound.org/apiv2/search/text/?query=" + term + "&token=06mS7W2OiXidVC2tQ4ikMfe3nomU7rBptaJgBCvp"))
    # test2 = json.load(urllib2.urlopen("https://api.jamendo.com/v3.0/tracks/?client_id=4cb8fab9&format=jsonpretty&name=" + term))
    # pprint(test)
    # pprint(test2)
    dictionary = PyDictionary()
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    #---------association-----------------------------------------------

    for rel in relations:

        sparql.setQuery("""
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dct: <http://purl.org/dc/terms/>
                PREFIX dbo: <http://dbpedia.org/ontology/>
                SELECT ?subject
                WHERE { <""" + dbresource + """> """+ rel +""" ?subject }
            """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print results

        sparql.setQuery("""
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dct: <http://purl.org/dc/terms/>
                PREFIX dbo: <http://dbpedia.org/ontology/>
                SELECT ?subject
                WHERE { ?subject """+ rel +""" <""" + dbresource + """> }
            """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print results
    # for result in results["results"]["bindings"]:
    #     print "++++++++++++++++++++++++++++++++++++"
    #     print(result["subject"]["value"])
    #     print "++++++++++++++++++++++++++++++++++++"
    #     sparql.setQuery("""
    #             PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    #             PREFIX dcterms: <http://purl.org/dc/terms/>
    #             SELECT ?subject ?label
    #             WHERE { ?subject """+ relation +""" <""" + result["subject"]["value"] + """>.}
    #             LIMIT 5
    #             """)
    #     sparql.setReturnFormat(JSON)
    #     results2 = sparql.query().convert()
    #     for result2 in results2["results"]["bindings"]:
    #         print(result2["subject"]["value"].replace("http://dbpedia.org/resource/", ""))
    #         expandedTerm = result2["subject"]["value"].replace("http://dbpedia.org/resource/", "")
            #test = json.load(urllib2.urlopen("http://www.freesound.org/apiv2/search/text/?query=" + expandedTerm + "&token=06mS7W2OiXidVC2tQ4ikMfe3nomU7rBptaJgBCvp"))
            #pprint (test)

    # ---------creator-----------------------------------------------

    # sparql.setQuery("""
    #         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    #         PREFIX dcterms: <http://purl.org/dc/terms/>
    #         SELECT ?subject
    #         WHERE { <http://dbpedia.org/resource/""" + term + """> dbo:composerOf ?subject }
    #     """)
    # sparql.setReturnFormat(JSON)
    # results = sparql.query().convert()
    # print results
    return results


#-------------------AT--------------------------------------------------------------------------------------------------

def dpbediaQueryTypeAT(resource, relations):
    print 'Query type AT'
    dbresource = resource
    print "dbresource is %s" % dbresource
    print "relation is %s" % relations
    # test = json.load(urllib2.urlopen("http://www.freesound.org/apiv2/search/text/?query=" + term + "&token=06mS7W2OiXidVC2tQ4ikMfe3nomU7rBptaJgBCvp"))
    # test2 = json.load(urllib2.urlopen("https://api.jamendo.com/v3.0/tracks/?client_id=4cb8fab9&format=jsonpretty&name=" + term))
    # pprint(test)
    # pprint(test2)
    dictionary = PyDictionary()
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    for rel in relations:

        sparql.setQuery("""
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dct: <http://purl.org/dc/terms/>
                PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX dbp: <http://dbpedia.org/property/>
                SELECT ?subject
                WHERE { <""" + dbresource + """> """+ rel +""" ?subject }
            """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print results

        sparql.setQuery("""
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX dct: <http://purl.org/dc/terms/>
                PREFIX dbo: <http://dbpedia.org/ontology/>
                PREFIX dbp: <http://dbpedia.org/property/>
                SELECT ?subject
                WHERE { ?subject """+ rel +""" <""" + dbresource + """> }
            """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print results


#----------------------------LIKE---------------------------------------------------------------------------------------


def dpbediaQueryTypeLIKE(query):
    term = query
    synonyms=[]
    print 'Query type LIKE'
    for lemma in wn.synset(term+'.n.01').lemmas():
        print lemma.name()
        synonyms.append(lemma.name())
    return synonyms


#----------------FOR----------------------------------------------------------------------------------------------------


def dpbediaQueryTypeFOR(resource, relations):
    print 'Query type FOR'
    dbresource = resource
    print "dbresource is %s" % dbresource
    print "relation is %s" % relations
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    for rel in relations:
        sparql.setQuery("""
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX dct: <http://purl.org/dc/terms/>
                    PREFIX dbo: <http://dbpedia.org/ontology/>
                    PREFIX dbp: <http://dbpedia.org/property/>
                    SELECT ?subject
                    WHERE { <""" + dbresource + """> """ + rel + """ ?subject }
                """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print results

        sparql.setQuery("""
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX dct: <http://purl.org/dc/terms/>
                    PREFIX dbo: <http://dbpedia.org/ontology/>
                    PREFIX dbp: <http://dbpedia.org/property/>
                    SELECT ?subject
                    WHERE { ?subject """ + rel + """ <""" + dbresource + """> }
                """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print results

#---------------FROM----------------------------------------------------------------------------------------------------

def dpbediaQueryTypeFROM(resource, relations):
    print 'Query type FROM'
    dbresource = resource
    print "dbresource is %s" % dbresource
    print "relation is %s" % relations
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    for rel in relations:
        sparql.setQuery("""
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX dct: <http://purl.org/dc/terms/>
                        PREFIX dbo: <http://dbpedia.org/ontology/>
                        PREFIX dbp: <http://dbpedia.org/property/>
                        SELECT ?subject
                        WHERE { <""" + dbresource + """> """ + rel + """ ?subject }
                    """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print results

        sparql.setQuery("""
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX dct: <http://purl.org/dc/terms/>
                        PREFIX dbo: <http://dbpedia.org/ontology/>
                        PREFIX dbp: <http://dbpedia.org/property/>
                        SELECT ?subject
                        WHERE { ?subject """ + rel + """ <""" + dbresource + """> }
                    """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print results

#-----------------------------BY----------------------------------------------------------------------------------------


def dpbediaQueryTypeBY(resource, relations ):
    print 'Query type BY'
    dbresource = resource
    print "dbresource is %s" % dbresource
    print "relation is %s" % relations
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    for rel in relations:
        sparql.setQuery("""
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX dct: <http://purl.org/dc/terms/>
                        PREFIX dbo: <http://dbpedia.org/ontology/>
                        PREFIX dbp: <http://dbpedia.org/property/>
                        SELECT ?subject
                        WHERE { <""" + dbresource + """> """ + rel + """ ?subject }
                    """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print results
        sparql.setQuery("""
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        PREFIX dct: <http://purl.org/dc/terms/>
                        PREFIX dbo: <http://dbpedia.org/ontology/>
                        PREFIX dbp: <http://dbpedia.org/property/>
                        SELECT ?subject
                        WHERE { ?subject """ + rel + """ <""" + dbresource + """> }
                    """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print results


#-----------------------------BEFORE------------------------------------------------------------------------------------


def dpbediaQueryTypeBEFORE(resource, relations):
    print 'Query type BEFORE'
    dbresource = resource
    print "dbresource is %s" % dbresource
    print "relation is %s" % relations
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    for rel in relations:
        sparql.setQuery("""
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            PREFIX dct: <http://purl.org/dc/terms/>
                            PREFIX dbo: <http://dbpedia.org/ontology/>
                            PREFIX dbp: <http://dbpedia.org/property/>
                            SELECT ?subject
                            WHERE { <""" + dbresource + """> """ + rel + """ ?subject }
                        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print results
        sparql.setQuery("""
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            PREFIX dct: <http://purl.org/dc/terms/>
                            PREFIX dbo: <http://dbpedia.org/ontology/>
                            PREFIX dbp: <http://dbpedia.org/property/>
                            SELECT ?subject
                            WHERE { ?subject """ + rel + """ <""" + dbresource + """> }
                        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print results
    #return results


#-------------------------------IN--------------------------------------------------------------------------------------


def dpbediaQueryTypeIN(resource, relations):
    print 'Query type IN'
    dbresource = resource
    print "dbresource is %s" % dbresource
    print "relation is %s" % relations
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    for rel in relations:
        sparql.setQuery("""
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            PREFIX dct: <http://purl.org/dc/terms/>
                            PREFIX dbo: <http://dbpedia.org/ontology/>
                            PREFIX dbp: <http://dbpedia.org/property/>
                            SELECT ?subject
                            WHERE { <""" + dbresource + """> """ + rel + """ ?subject }
                        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print results
        sparql.setQuery("""
                            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                            PREFIX dct: <http://purl.org/dc/terms/>
                            PREFIX dbo: <http://dbpedia.org/ontology/>
                            PREFIX dbp: <http://dbpedia.org/property/>
                            SELECT ?subject
                            WHERE { ?subject """ + rel + """ <""" + dbresource + """> }
                        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print results
    #return results


#dpbediaQuery("of London")