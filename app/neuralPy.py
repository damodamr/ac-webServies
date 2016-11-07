#import neuralpy
#import word2vecKeras
#from word2veckeras import Word2VecKeras
import gensim, logging, os
from nltk.corpus import brown
import nltk

#net = neuralpy.Network([2, 10, 8, 1])
datum_1 = ([1, 1], [0])
datum_2 = ([1, 0], [1])
datum_3 = ([0, 1], [1])
datum_4 = ([0, 0], [0])

dataset = [datum_1, datum_2, datum_3, datum_4]
epochs = 5000
learning_rate = 3
#net.train(dataset, epochs, learning_rate, monitor = True)
#net.show_cost()
#print net.forward([1,0])

#for x, y in dataset:
    #print net.forward(x)

#vsk = Word2VecKeras(gensim.models.word2vec.LineSentence('test.txt'),iter=100)
#print( vsk.most_similar('the', topn=5))


#brk = Word2VecKeras(brown.sents(),iter=10)
#print( brk.most_similar('the', topn=5))

# import modules & set up logging

emma = nltk.corpus.gutenberg.sents('austen-emma.txt')
sentences = emma
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# train word2vec on the two sentences
model = gensim.models.Word2Vec(sentences, min_count=1)





# a memory-friendly iterator
#model = gensim.models.Word2Vec(sentences, min_count=10, size=200, workers=4)
#model = gensim.models.Word2Vec.load_word2vec_format(emma, binary=False)

print (model.similarity('sound', 'tree'))
print (model.most_similar(positive=['sound', 'music'], negative=['tree'], topn=1))
print (model.doesnt_match("sound tree house painting").split())