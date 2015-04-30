from nltk.corpus import treebank
train_data = treebank.tagged_sents()[:3000]
test_data = treebank.tagged_sents()[3000:]

from nltk.tag import tnt
tnt_pos_tagger = tnt.TnT()
tnt_pos_tagger.train(train_data)

import pickle

f = open('pos_tagger.pickle', 'w')
pickle.dump(tnt_pos_tagger, f)
f.close()