import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities
dictionary = corpora.Dictionary.load('C:/word2vec/deerwester.dict')
corpus = corpora.MmCorpus('C:/word2vec/deerwester.mm') # comes from the first tutorial, "From strings to vectors"
print(corpus)