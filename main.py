from Tkinter import Tk, Text, BOTH, Menu, W, N, E, S, INSERT, END, Toplevel, Message
import re, math, collections, itertools, os
import pickle
from ttk import Frame
import interface
import naiveBayesModel
import decisionTreeModel
import multinomialNBModel
import logicalRegression
import svcModel

class mainInterface():
    def main():
        root = Tk()
        interface.createUI(root)
        app = interface.Example(root)
        root.mainloop()  
        
    ##############################
    ##Classifier Trainers(button callbacks)
    ##############################
    def trainNB(self):
        nbModel = naiveBayesModel.Model()
        nbModel.trainNaiveBayes()
        
    def trainDT(self):
        dtModel = decisionTreeModel.Model()
        dtModel.trainDecisionTree()
        
    def trainMultiNB(self):
        multiNBModel = multinomialNBModel.Model()
        multiNBModel.trainMultinomialNB()
        
    def trainSVC(self):
		vectorModel = svcModel.Model()
		vectorModel.trainSVC()
        
    
    ##############################
    ##Classifier Use Functions(button callbacks)
    ##############################
    def analyzeNB(self, area, posneg):
        inp = area.get("1.0",'end-1c')
        wordList = re.sub("[^\w]", " ",  inp).split()
        feats = dict([(word, True) for word in wordList])
        #load trained classifier
        f = open('nbclassifier.pickle')
        classifier = pickle.load(f)
        f.close
        #insert pos/neg into txtbox
        posneg.delete(1.0, END)
        posneg.insert(INSERT, classifier.classify(feats))
        print classifier.classify(feats)
        
    def analyzeNB_nltk(self, area, posneg):
        inp = area.get("1.0",'end-1c')
        wordList = re.sub("[^\w]", " ",  inp).split()
        feats = dict([(word, True) for word in wordList])
        #load trained classifier
        f = open('nbclassifier_nltk.pickle')
        classifier = pickle.load(f)
        f.close
        #insert pos/neg into txtbox
        posneg.delete(1.0, END)
        posneg.insert(INSERT, classifier.classify(feats))
        print classifier.classify(feats)
        
    def analyzeSVC(self, area, posneg):
        inp = area.get("1.0",'end-1c')
        wordList = re.sub("[^\w]", " ",  inp).split()
        feats = dict([(word, True) for word in wordList])
        #load trained classifier
        f = open('svcclassifier.pickle')
        classifier = pickle.load(f)
        f.close
        #insert pos/neg into txtbox
        posneg.delete(1.0, END)
        posneg.insert(INSERT, classifier.classify(feats))
        print classifier.classify(feats)
        
    def analyzeDecisionTree_nltk(self, area, posneg):
        inp = area.get("1.0",'end-1c')
        wordList = re.sub("[^\w]", " ",  inp).split()
        feats = dict([(word, True) for word in wordList])
        #load trained classifier
        f = open('decisionTreeClassifier_nltk.pickle')
        classifier = pickle.load(f)
        f.close
        #insert pos/neg into txtbox
        posneg.delete(1.0, END)
        posneg.insert(INSERT, classifier.classify(feats))
        print classifier.classify(feats)
        
    def analyzeMultiNB_nltk(self, area, posneg):
        inp = area.get("1.0",'end-1c')
        wordList = re.sub("[^\w]", " ",  inp).split()
        feats = dict([(word, True) for word in wordList])
        #load trained classifier
        f = open('multiNB.pickle')
        classifier = pickle.load(f)
        f.close
        #insert pos/neg into txtbox
        posneg.delete(1.0, END)
        posneg.insert(INSERT, classifier.classify(feats))
        print classifier.classify(feats)
        
    def analyzeLogReg(self, area, scorebox2):
        inp = area.get("1.0",'end-1c')
        #self.calc_log_regression(inp)
        l = logicalRegression.Regression()
        test = l.calc_log_regression(inp)
        scorebox2.delete(1.0, END)
        scorebox2.insert(INSERT, test)
    
    def showStats(self, area2):
        statsRecordNB = open('statsRecordNB.txt', 'r')
        statsNB = statsRecordNB.read()
        area2.insert(INSERT, "NAIVE BAYES STATISTICS\n")
        area2.tag_add("Blue", "1.0", "1.22")
        area2.tag_config("Blue", background="black", foreground="blue")
        area2.insert(INSERT, statsNB)
      
    ##############################
    ##End Classifier Use Functions
    ##############################




    if __name__ == '__main__':
        main()
