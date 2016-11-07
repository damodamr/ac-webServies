from textblob import TextBlob, Word
import spotlight
from nltk.corpus import wordnet as wn


#print (Word(term))
#print(Word(term).definitions)

def spotlightSearch(term):
    spotlightTerms = []
    words = TextBlob(term).words
    #print words

    for word in words:
        try:
            annotations = spotlight.annotate('http://spotlight.sztaki.hu:2222/rest/annotate',word,confidence=0.3, support=20, spotter='Default')
            #print word, '\t', annotations[0].get('URI'), '\t', (wn.synset(word+'.n.01').definition()), '\t',(wn.synset(word+'.n.01').hypernyms() )
            spotlightTerms.append(word)
            spotlightTerms.append(annotations[0].get('URI'))
            spotlightTerms.append(wn.synset(word+'.n.01').definition())
            spotlightTerms.append(wn.synset(word+'.n.01').hypernyms())
            #spotlightTerms.append(wn.synset(word + '.n.01').hyponyms())
            print word, annotations[0].get('URI')
        except:
            #print word, '\t', "Nothing"
            pass

    #print spotlightTerms
    return annotations

#term = "London night"
#spotlightSearch(term)