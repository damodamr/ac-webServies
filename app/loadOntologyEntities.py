import rdflib

moSub = []
moPred = []
moObj = []

def query():
    g = rdflib.Graph()
    mo = g.parse("http://purl.org/ontology/mo/")
    for subj, pred, obj in mo:
            moSub.append(subj)
            moPred.append(pred)
            moObj.append(obj)
    return moSub,moPred,moObj
