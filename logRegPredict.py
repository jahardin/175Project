import os
import nltk
import numpy

dataDir = r"C:\aclImdb"

print "Reading training set..."

# get svm vocab words

f = open('logRegVocab.txt', 'r')
word_features = f.read().splitlines()
f.close()

f2 = open('logRegScale.txt', 'r')
word_scale = [float(i) for i in f2.read().splitlines()]
f2.close()

def bow_features(document):
	words = nltk.word_tokenize(document)
	print len(words)
	features = [0] * len(word_features)
	features[0] = 1	
	for word in words:
		if word in word_features:
			features[word_features.index(word)+1] += 1
	for i in range(len(features)):
		features[i] *= word_scale[i]/(len(words))
	
	return features

fw = open('logRegWeights.txt', 'r')
weights = [float(i) for i in fw.read().splitlines()]
fw.close()

def logReg(document):
	bow = bow_features(document)
	z = 0
	for i in range(0,len(bow)):
		z = z + bow[i] * weights[i]
	return 1 + 9 / (1 + numpy.exp(-z))

sent1 = "This movie is the best ever!"
sent2 = "This is a truly spectacular film. I would definitely see this movie again."
sent3 = "This film suffers from terrible acting and awful directing."
sent4 = "A decently funny movie with some serious shortcomings. Over all it was fairly good but not spectacular."



print logReg(sent1)
print logReg(sent2)
print logReg(sent3)
print logReg(sent4)
