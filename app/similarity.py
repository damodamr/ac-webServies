from textblob import TextBlob
from nltk.corpus import stopwords
from practnlptools.tools import Annotator
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.wsd import lesk


lmtzr = WordNetLemmatizer()
copula="capital"
type="settlement"
categoriesList={"articles including recorded pronunciations (uk english)","british capitals","capitals in europe","london", "populated places established in the 1st century","port cities and towns in england","staple ports"}

for category in categoriesList:
    term = TextBlob(category)
    print term.words
    for word in term.words:
        lemWord=lmtzr.lemmatize(word)
        print lemWord
        if copula in lemWord:
            print "Found"


sent = ['location']
for ss in wn.synsets('capital'):
    print(ss, ss.definition())

print "-----------------"
print(lesk(sent, "capital")).definition()

