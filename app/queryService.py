import json
import urllib2
from practnlptools.tools import Annotator
import re
import WordNet
import DBPedia
import pprint
import spotlight


def query(term):
    test = json.load(urllib2.urlopen("http://www.freesound.org/apiv2/search/text/?query="+term+"&token=06mS7W2OiXidVC2tQ4ikMfe3nomU7rBptaJgBCvp"))
    test2 = json.load(urllib2.urlopen("https://api.jamendo.com/v3.0/tracks/?client_id=4cb8fab9&format=jsonpretty&name="+term))

    return test, test2

def complexQuery(term):
    #test = json.load(urllib2.urlopen("http://www.freesound.org/apiv2/search/text/?query="+term+"&token=06mS7W2OiXidVC2tQ4ikMfe3nomU7rBptaJgBCvp"))
    #test2 = json.load(urllib2.urlopen("https://api.jamendo.com/v3.0/tracks/?client_id=4cb8fab9&format=jsonpretty&name="+term))

    annotator = Annotator()
    dep_parse = annotator.getAnnotations(term, dep_parse=True)['dep_parse']
    dp_list = dep_parse.split('\n')

    spotlightTerms = WordNet.spotlightSearch(term)
    print dp_list
    #spotlightTerms = spotlight.annotate('http://spotlight.sztaki.hu:2222/rest/annotate', term, confidence=0.3, support=20, spotter='Default')
    #print term, '\t', spotlightTerms[1].get('URI')
    #print spotlightTerms[0].get('URI')
    secondDep = ""
    query=[]

    for prep in dp_list:
        elementPrep = "prep"
        if elementPrep in prep:
            print ("We found preposition1: %s" % prep[prep.find("_") + 1:prep.find("(")])
            prepType=prep[prep.find("_") + 1:prep.find("(")]
            print ("We found preposition2: %s" % prep[prep.find(" ")+1:prep.find(")")])
            secondDep= prep[prep.find(" ")+1:prep.find(")")].split("-")
            print secondDep[0]
            query.append(prepType)
            query.append(secondDep[0])
            results = DBPedia.dpbediaQuery(query)
            print results


    #test = json.load(urllib2.urlopen("http://www.freesound.org/apiv2/search/text/?query=" + secondDep[0] + "&token=06mS7W2OiXidVC2tQ4ikMfe3nomU7rBptaJgBCvp"))
    #test2 = json.load(urllib2.urlopen("https://api.jamendo.com/v3.0/tracks/?client_id=4cb8fab9&format=jsonpretty&name=" + secondDep[0]))

    #print(test)
    #print(test2)

    return dp_list, spotlightTerms, results
    #return dp_list, spotlightTerms






term = "Sound of London"
#term = "Sound like Thunder"
#ner = annotator.getAnnotations(term)['ner']
#print ner
#complexQuery(term)