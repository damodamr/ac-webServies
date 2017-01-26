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



def wikiSearch(term):
    try:
        wiki = TextBlob(wikipedia.summary(term, sentences=1))
        print wiki
    except:
        pass



def readFile():
    input_file = open("C:\\Users\\Sergio\\Dropbox\\QMUL\\Data\\choicesNHS\\nhsChoices.txt", "r")
    #input_file = open("C:\\Users\\Sergio\\Dropbox\\QMUL\\Data\\choicesNHS\\nhsChoicesDiagnosis.txt", "r")
    #input_file = open("C:\\Users\\Sergio\\Dropbox\\QMUL\\Data\\choicesNHS\\nhsChoicesDiabetesWhole.txt", "r")
    lines = input_file.readlines()
    input_file.close()

    annotationsX = []
    annotationsSLR = []
    annotationsNER = []

    for x in lines:

        annotationX = x
        annotationSLR = annotator.getAnnotations(x,dep_parse=True)['srl']
        #annotationNER = annotator.getAnnotations(x,dep_parse=True)['ner']
        annotationsX.append(annotationX)
        annotationsSLR.append(annotationSLR)
        #annotationsNER.append(annotationNER)


    size = len(annotationsSLR)
    print size

    A0 = 0
    A1 = 0
    pbroles = []
    annotationsA0 = []
    annotationsA1 = []


    for an in range(5):
        print annotationsX[an]
        print annotationsSLR[an]
        sizeIn = len(annotationsSLR[an])
        #print sizeIn
        for an2 in range(sizeIn):

            print "--------------------------------------------------------------------------------------------------------"

            print annotationsSLR[an][an2]["V"]
            w = Word(annotationsSLR[an][an2]["V"]).lemmatize("v")
            #print w
            #print wn.synset(w+'.v.01')

            try:
                for role in propbank.roleset(w+'.01').findall("roles/role"):
                    print(role.attrib['f'], role.attrib['n'], role.attrib['descr'])
                    pbroles.append(role.attrib['descr'])
                #for role in propbank.roleset(w+'.01').findall("aliases/alias"):
                    #print(role.attrib['framenet'], role.attrib['pos'], role.attrib['verbnet'])
            except:
                pass

            try:
                print(wn.lemma(w+'.v.01.'+w).derivationally_related_forms())
            except:
                pass

            if "A0" in annotationsSLR[an][an2]:
                print annotationsSLR[an][an2]["A0"]
                A0 = annotationsSLR[an][an2]["A0"]
                #try:
                   #A0 = TextBlob(A0, np_extractor=extractor)
                    #A0 = A0.noun_phrases[0]
                    #print A0
                #except:
                    #pass
                try:
                    annotationsA0 = WordNet.spotlightSearch(A0)
                    annotationsA0 = annotationsA0[0].get('URI')
                except:
                    annotationsA0 = "unknown"
                    pass

            if "A1" in annotationsSLR[an][an2]:
                print annotationsSLR[an][an2]["A1"]
                A1 = annotationsSLR[an][an2]["A1"]
                #try:
                    #A1 = TextBlob(A1, np_extractor=extractor)
                    #A1 = A1.noun_phrases[0]
                    #print A1
                #except:
                    #pass
                try:
                    annotationsA1 = WordNet.spotlightSearch(A1)
                    annotationsA1 = annotationsA1[0].get('URI')
                except:
                    annotationsA1 = "unknown"
                    pass


            print pbroles


            print "--------------------------------------------------------------------------------------------------------"

            CreateGraphNeo4J.createGraph(w, A0, A1, pbroles, annotationsA0, annotationsA1)
            del pbroles[:]
            annotationsA0 = []
            annotationsA1 = []
            A0 = 0
            A1 = 0


readFile()

#annotations = WordNet.spotlightSearch("body 's cells")
#print annotations[0].get('URI')