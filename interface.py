from Tkinter import Tk, Text, BOTH, Menu, W, N, E, S, INSERT, END
import os, random
from ttk import Frame, Button, Label, Style
import tkFileDialog
from tkFileDialog import askopenfilename
import re, math, collections, itertools, os
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier, DecisionTreeClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
import pickle
from sklearn.svm import LinearSVC

#filepaths
DIR_ROOT = '/home/jacobus/Desktop/175Project'
POS_FILE = os.path.join(DIR_ROOT, 'combinedPos')
NEG_FILE = os.path.join(DIR_ROOT, 'combinedNeg')

#globals
best_words = set();

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
    def initUI(self):
        
        #BUTTON CALLBACKS
        def giveRandom():
            print random.choice(os.listdir("C:\\test\neg"))

        #MENU
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen)
        menubar.add_cascade(label="File", menu=fileMenu) 
        
        self.parent.title("IMDB Sentiment Analysis")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        #ROWS/COLUMNS
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1, pad=20)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, pad=5)
        self.rowconfigure(3, pad=5)
        self.rowconfigure(4, pad=5)
        self.rowconfigure(5, pad=5)
        
        #LEFT TEXTBOX
        self.area = Text(self)
        self.area.grid(row=0, column=0, columnspan=1, rowspan=6, 
            padx=5, sticky=E+W+S+N)
        
        #RIGHT TEXTBOX
        self.area2 = Text(self)
        self.area2.grid(row=0, column=2, columnspan=1, rowspan=6, 
            padx=5, sticky=W+E+S+N)
        
        #SCORES/LABELS
        lbl = Label(self, text="Actual Score")
        lbl.grid(row=3, column=1, sticky=W, pady=4, padx=5)
        self.scorebox = Text(self, width=2, height=1)
        self.scorebox.grid(row=3, column=1, sticky=E)
        
        lbl2 = Label(self, text="Our Score")
        lbl2.grid(row=4, column=1, sticky=W, pady=4, padx=5)
        self.scorebox2 = Text(self, width=2, height=1)
        self.scorebox2.grid(row=4, column=1, sticky=E)
        
        lbl3 = Label(self, text="Sentiment")
        lbl3.grid(row=5, column=1, sticky=W)
        self.posneg = Text(self, width=3, height=1)
        self.posneg.grid(row=5, column=1, sticky=E)
        
        #BUTTONS
        abtn = Button(self, text="AnalyzeNB", command=self.analyzeNB)
        abtn.grid(row=0, column=1, sticky=N+W)
        bbtn = Button(self, text="AnalyzeSVC", command=self.analyzeSVC)
        bbtn.grid(row=0, column=1, sticky=N+E)
        gbtn = Button(self, text="Generate")
        gbtn.grid(row=1, column=1, sticky=N) 
        ggbtn = Button(self, text="Random", command=giveRandom)
        ggbtn.grid(row=2, column=1, sticky=N)
        trainnbbtn = Button(self, text="TrainClassifiers", command=self.trainNaiveBayes)
        trainnbbtn.grid(row=0, column=1, sticky=S)
    #end initUI(self)
    
    ####################
    #INTERFACE FUNCTIONS
    ####################
    def onOpen(self):
        ftypes = [('Text Files', '*.txt'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()

        if fl != '':
            text = self.readFile(fl)
            self.area.delete(1.0, END)
            self.area.insert(END, text)

    def readFile(self, filename):
        f = open(filename, "r")
        text = f.read()
        filenamearr = filename.split("_")
        score = filenamearr[1].split(".")
        self.scorebox.delete(1.0, END)
        self.scorebox.insert(INSERT, score[0])
        #print "score " + score[0]
        return text
        
    def analyzeNB(self):
        inp = self.area.get("1.0",'end-1c')
        wordList = re.sub("[^\w]", " ",  inp).split()
        feats = dict([(word, True) for word in wordList])
        #load trained classifier
        f = open('nbclassifier.pickle')
        classifier = pickle.load(f)
        f.close
        #insert pos/neg into txtbox
        self.posneg.delete(1.0, END)
        self.posneg.insert(INSERT, classifier.classify(feats))
        print classifier.classify(feats)
        
    def analyzeSVC(self):
        inp = self.area.get("1.0",'end-1c')
        wordList = re.sub("[^\w]", " ",  inp).split()
        feats = dict([(word, True) for word in wordList])
        #load trained classifier
        f = open('svcclassifier.pickle')
        classifier = pickle.load(f)
        f.close
        #insert pos/neg into txtbox
        self.posneg.delete(1.0, END)
        self.posneg.insert(INSERT, classifier.classify(feats))
        print classifier.classify(feats)
    ####################
    #END INTERFACE FUNCTIONS
    ####################
    
	##########################
	#CLASSIFIER FUNCTIONS
	##########################
    def trainNaiveBayes(self):
        numbers_to_test = [10, 100, 1000, 10000, 15000]
        wordScores = self.create_word_scores()
        print 'using all words as features'
        self.evaluate_features(self.make_full_dict)
        for num in numbers_to_test:
            print 'evaluating best %d word features' % (num)
            best_words = self.find_best_words(wordScores, num)
            #print best_words
            self.evaluate_features(self.best_word_features)
            
    def best_word_features(self, words):
        return dict([(word, True) for word in words if word in best_words])
    
    def make_full_dict(self, words):
        return dict([(word, True) for word in words])
    
    def evaluate_features(self, feature_select):
        posFeatures=[]
        negFeatures=[]
        with open(POS_FILE, 'r') as posSentences:
            for i in posSentences:
                posWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
                posWords = [feature_select(posWords), 'pos']
                posFeatures.append(posWords)
        with open(NEG_FILE, 'r') as negSentences:
            for i in negSentences:
                negWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
                negWords = [feature_select(negWords), 'neg']
                negFeatures.append(negWords)
    
        #3/4 of features for training, 1/4 for testing
        posCutoff = int(math.floor(len(posFeatures)*3/4))
        negCutoff = int(math.floor(len(negFeatures)*3/4))
        trainFeatures = posFeatures[:posCutoff] + negFeatures[:negCutoff]
        testFeatures = posFeatures[posCutoff:] + negFeatures[negCutoff:]
        
        ######
        #CLASSIFIER
        ######
        #train the Classifiers
        classifier = NaiveBayesClassifier.train(trainFeatures)
        svcclassifier = nltk.classify.SklearnClassifier(LinearSVC())
        svcclassifier.train(trainFeatures)
        
        #save classifiers for later
        f = open('nbclassifier.pickle', 'wb')
        pickle.dump(classifier, f)
        f.close()
        ff = open('svcclassifier.pickle', 'wb')
        pickle.dump(svcclassifier, ff)
        ff.close()
        
        #make reference set and test sets
        referenceSets = collections.defaultdict(set)
        testSets = collections.defaultdict(set)
        
        #put correctly labeled sentences in reference, predictively labeled in test sets
        for i, (features, label) in enumerate(testFeatures):
            referenceSets[label].add(i)
            predicted = classifier.classify(features)
            testSets[predicted].add(i)
        
        #prints metrics to show how well the feature selection did
        print 'train on %d instances, test on %d instances' % (len(trainFeatures), len(testFeatures))
        print ' accuracy:', nltk.classify.util.accuracy(classifier, testFeatures)
        print 'pos precision:', nltk.metrics.precision(referenceSets['pos'], testSets['pos'])
        print 'pos recall:', nltk.metrics.recall(referenceSets['pos'], testSets['pos'])
        print 'neg precision:', nltk.metrics.precision(referenceSets['neg'], testSets['neg'])
        print 'neg recall:', nltk.metrics.recall(referenceSets['neg'], testSets['neg'])
        classifier.show_most_informative_features(10)
    #end evaluate_features(feature_select)
    
    def create_word_scores(self):
        #make list of pos and neg words
        posWords=[]
        negWords=[]
        with open(POS_FILE, 'r') as posSentences:
            for i in posSentences:
                posWord = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
                posWords.append(posWord)
    	with open(NEG_FILE, 'r') as negSentences:
            for i in negSentences:
                negWord = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
                negWords.append(negWord)
        posWords = list(itertools.chain(*posWords))
        negWords = list(itertools.chain(*negWords))
        
        #build freq dist of all words, then of words with pos/neg labels
        word_fd = FreqDist()
        cond_word_fd = ConditionalFreqDist()
        for word in posWords:
            word_fd[word.lower()] += 1
            cond_word_fd['pos'][word.lower()] += 1
        for word in negWords:
            word_fd[word.lower()] += 1
            cond_word_fd['neg'][word.lower()] += 1
        
        #finds num of pos and neg words/total num of words
        pos_word_count = cond_word_fd['pos'].N()
        neg_word_count = cond_word_fd['neg'].N()
        total_word_count = pos_word_count + neg_word_count
        
        #build dict of words based on chi-squared test    
        word_scores = {}
        for word, freq in word_fd.iteritems():
            pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
            neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count), total_word_count)    
            word_scores[word] = pos_score + neg_score
            
        return word_scores
    #end create_word_scores(self)
    
    def find_best_words(self, word_scores, number):
        wordScores = self.create_word_scores()
        best_vals = sorted(wordScores.iteritems(), key=lambda (w,s):s, reverse=True)[:number]
        global best_words; 
        best_words = set([w for w, s in best_vals])
        return best_words
    ##########################
    #END CLASSIFIER FUNCTIONS
    ##########################

def main():
    root = Tk()
    #root.geometry("500x500+500+500")
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()

    root.geometry("%dx%d+0+0" % (w, h))
    app = Example(root)
    root.mainloop()  
    
if __name__ == '__main__':
    main()
