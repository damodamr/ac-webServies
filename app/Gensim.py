from gensim import corpora, models, similarities

documents = ["Articles including recorded pronunciations",
"British capitals",
"Capitals in Europe",
"London",
"Populated places established in the 1st century",
"Port cities and towns in England",
"Staple ports"]

stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
          for document in documents]

from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
         frequency[token] += 1

texts = [[token for token in text if frequency[token] > 0]
          for text in texts]
from pprint import pprint
pprint(texts)

dictionary = corpora.Dictionary(texts)
dictionary.save('C:/WikipediaDump/deerwester.dict')
print(dictionary)
print(dictionary.token2id)

new_doc = "Human computer interaction"
new_vec = dictionary.doc2bow(new_doc.lower().split())
print(new_vec)

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('C:/WikipediaDump/deerwester.mm', corpus)
print(corpus)

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)

doc = "capital"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow] # convert the query to LSI space
print(vec_lsi)

index = similarities.MatrixSimilarity(lsi[corpus])

sims = index[vec_lsi] # perform a similarity query against the corpus
print(list(enumerate(sims)))

sims = sorted(enumerate(sims), key=lambda item: -item[1])
print(sims)

import os.path
from gensim import corpora, models, similarities
if (os.path.exists("C:/WikipediaDump/deerwester.dict")):
    dictionary = corpora.Dictionary.load('C:/WikipediaDump/deerwester.dict')
    corpus = corpora.MmCorpus('C:/WikipediaDump/deerwester.mm')
    print("Used files generated from first tutorial")
else:
    print("Please run first tutorial to generate data set")

tfidf = models.TfidfModel(corpus)

doc_bow = [(0, 1), (1, 1)]
print(tfidf[doc_bow])

corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
     print(doc)

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2) # initialize an LSI transformation
corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

print (lsi.print_topics(2))

for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
     print(doc)

lsi.save('C:/WikipediaDump/model.lsi')

from gensim import corpora, models, similarities
dictionary = corpora.Dictionary.load('C:/WikipediaDump/deerwester.dict')
corpus = corpora.MmCorpus('C:/WikipediaDump/deerwester.mm') # comes from the first tutorial, "From strings to vectors"
print(corpus)

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
doc = "uk"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow] # convert the query to LSI space
print(vec_lsi)

index = similarities.MatrixSimilarity(lsi[corpus]) # transform corpus to LSI space and index it

index.save('C:/WikipediaDump/deerwester.index')
index = similarities.MatrixSimilarity.load('C:/WikipediaDump/deerwester.index')

sims = index[vec_lsi] # perform a similarity query against the corpus
print(list(enumerate(sims)))

sims = sorted(enumerate(sims), key=lambda item: -item[1])
print(sims)