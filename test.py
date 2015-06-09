import logging
import numpy as np
from optparse import OptionParser
import sys
import re
from time import time
import matplotlib.pyplot as plt
from itertools import chain
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.extmath import density
from sklearn import metrics
from sklearn.svm import libsvm

categories = ['pos', 'neg']

data_train = ["great movie", "awesome movie", "horrible never watch again", "bad movie"]
data_train_target = [1, 1, 0, 0]

data_test = ["great to watch", "awesome to watch", "horrible to watch", "bad to watch"]
data_test_target = [1, 1, 0, 0]

#load positive and negative words
posFeatures = []
negFeatures = []
allFeatures = []
with open('combinedPos', 'r') as posSentences:
	for i in posSentences:
		posWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
		posFeatures.append(posWords)
		allFeatures.append(posWords)
with open('combinedNeg', 'r') as negSentences:
	for i in negSentences:
		negWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
		negFeatures.append(negWords)
		allFeatures.append(negWords)
		
	
#assign appropriate number of 1's and 0's
dataTrainTarget = []
for i in posFeatures:
	dataTrainTarget.append(1)
for i in negFeatures:
	dataTrainTarget.append(0)

#split into training and test set
y_train, y_test = data_train_target, data_test_target
#y_train, y_test = dataTrainTarget, data_test_target

#extract features from training data using sparse vectorizer
vectorizer = HashingVectorizer(stop_words='english', non_negative=True)
X_train = vectorizer.fit_transform(data_train)
#X_train = vectorizer.fit_transform(allFeatures)

#extract features from test data using same vectorizer
X_test = vectorizer.transform(data_test)

# Benchmark classifiers
def benchmark(clf):
    print('_' * 80)
    print("Training: ")
    print(clf)
    t0 = time()
    clf.fit(X_train, y_train)
    train_time = time() - t0
    print("train time: %0.3fs" % train_time)

    t0 = time()
    pred = clf.predict(X_test)
    test_time = time() - t0
    print("test time:  %0.3fs" % test_time)

    score = metrics.accuracy_score(y_test, pred)
    print("accuracy:   %0.3f" % score)

    print()
    clf_descr = str(clf).split('(')[0]
    return clf_descr, score, train_time, test_time


#benchmark the classifiers
results = []
for clf, name in (
        (RidgeClassifier(tol=1e-2, solver="lsqr"), "Ridge Classifier"),
        (Perceptron(n_iter=50), "Perceptron"),
        (PassiveAggressiveClassifier(n_iter=50), "Passive-Aggressive"),
        (KNeighborsClassifier(n_neighbors=4), "kNN"),
        (RandomForestClassifier(n_estimators=100), "Random forest")):
    print('=' * 80)
    print(name)
    results.append(benchmark(clf))
    
for penalty in ["l2", "l1"]:
    print('=' * 80)
    print("%s penalty" % penalty.upper())
    # Train Liblinear model
    results.append(benchmark(LinearSVC(loss='l2', penalty=penalty,
                                            dual=False, tol=1e-3)))

print('=' * 80)
print("LinearSVC with L1-based feature selection")
# The smaller C, the stronger the regularization.
# The more regularization, the more sparsity.
results.append(benchmark(Pipeline([
  ('feature_selection', LinearSVC(penalty="l1", dual=False, tol=1e-3)),
  ('classification', LinearSVC())
])))



# make some plots

indices = np.arange(len(results))

results = [[x[i] for x in results] for i in range(4)]

clf_names, score, training_time, test_time = results
training_time = np.array(training_time) / np.max(training_time)
test_time = np.array(test_time) / np.max(test_time)

plt.figure(figsize=(12, 8))
plt.title("Score")
plt.barh(indices, score, .2, label="score", color='r')
plt.barh(indices + .3, training_time, .2, label="training time", color='g')
plt.barh(indices + .6, test_time, .2, label="test time", color='b')
plt.yticks(())
plt.legend(loc='best')
plt.subplots_adjust(left=.25)
plt.subplots_adjust(top=.95)
plt.subplots_adjust(bottom=.05)

for i, c in zip(indices, clf_names):
    plt.text(-.3, i, c)

plt.show()
