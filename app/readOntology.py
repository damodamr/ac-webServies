import rdflib, datetime
from random import randrange
from rdflib import URIRef, BNode, Literal, Namespace, RDF, Graph
#g = Graph()
#g.parse("C:\Users\Sergio\Dropbox\QMUL\Data\searchOntology.owl", format="xml")

#len(g) # prints 2

import pprint
#for stmt in g:
    #pprint.pprint(stmt)




moSub = []
moPred = []
moObj = []

def query():
    g = rdflib.Graph()
    mo = g.parse("C:\Users\Sergio\Dropbox\QMUL\Data\searchOntology.owl")
    for subj, pred, obj in mo:
            moSub.append(subj)
            moPred.append(pred)
            moObj.append(obj)
            print "Subject: " + subj
            print "Predicate: " + pred
            print "Object: " + obj

def writeRDF(self, stateCreateR, stateCreateO, file, newSound):
    i = datetime.datetime.now()
    id=randrange(0, 1000)
    date = URIRef("http://purl.org/dc/terms/created")
    availableAs = URIRef("http://purl.org/ontology/mo/available_as")
    fileOriginal = URIRef("http://purl.org/ontology/mo/AudioFile/"+file)
    audioFile = URIRef("http://purl.org/ontology/mo/AudioFile")
    change = URIRef("http://example.org/mvco/" + stateCreateR + "/" + str(id))
    licence1 = URIRef("http://example.org/Permition/" + "CC0")
    licence2 = URIRef("http://example.org/Permition/" + stateCreateO)
    newFile = URIRef("http://purl.org/ontology/mo/AudioFile/"+newSound)
    acUser = URIRef("http://example.org/people/"+str(self))
    orUser = URIRef("http://example.org/people/" + file)

    RDF.type # = rdflib.term.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type')

    dateLit = Literal(i)

    ac = Namespace("http://example.org/ac/")
    mo = Namespace("http://purl.org/ontology/mo/")
    mvco = Namespace("http://purl.oclc.org/NET/mvco#")
    FOAF = Namespace("http://xmlns.com/foaf/0.1/")

    #n.acUser # = rdflib.term.URIRef(u'http://example.org/people/bob')
    g = Graph()

    g.add((newFile, RDF.type, audioFile))
    g.add((fileOriginal, RDF.type, audioFile))

    g.add((acUser, RDF.type, FOAF.Person))
    g.add((orUser, RDF.type, FOAF.Person))

    g.add((change, mvco.resultsIn, newFile) )
    g.add((change, mvco.actedOver, fileOriginal))
    g.add((change, mvco.actedBy, acUser))
    g.add((change, date, dateLit))

    g.add((licence1, mvco.permitsAction, change))
    g.add((licence1, mvco.issuedBy, fileOriginal))
    g.add((licence2, mvco.permitsAction, change))
    g.add((licence2, mvco.issuedBy, acUser))

    output =  str(g.serialize(format='n3'))

    print g.serialize(format='n3')

    return output

#writeRDF("test4", "remix", "CCBY", "338843", "fantastic")