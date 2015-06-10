from Tkinter import Tk, Text, BOTH, Menu, W, N, E, S, INSERT, END, Toplevel, Message
import os, random
from ttk import Frame, Button, Label, Style, Entry
import tkFileDialog
from tkFileDialog import askopenfilename
import re, math, collections, itertools, os
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier, DecisionTreeClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
import pickle
from sklearn.svm import LinearSVC
import threading
import numpy
import logicalRegression
import main

#globals
best_words = set()

#Main interface model to access all classifier functions for button callbacks
mainInterface = main.mainInterface()

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        self.markovGenerator = None
        self.markovStarting = False
        self.attemptedMarkov = False
        threading.Thread(target=self.startMarkov).start()

    def startMarkov(self):
        self.markovStarting = True
        from GenMarkov import GenMarkov
        self.markovGenerator = GenMarkov()
        self.markovStarting = False
        if self.attemptedMarkov:
            self.area.delete(1.0, END)
            self.area.insert(1.0, self.markovGenerator.GenRandom())

    def initUI(self):
        
        #BUTTON CALLBACKS
        def genRandom():
            if not self.markovStarting:
                self.area.delete(1.0, END)
                self.area.insert(1.0, self.markovGenerator.GenRandom())
            else:
                self.showLoading()

        def genSeed():
            if not self.markovStarting:
                self.area.delete(1.0, END)
                seed = seedEntry.get()
                self.area.insert(1.0, self.markovGenerator.GenSeed(seed))

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
        self.rowconfigure(1, pad=5)
        self.rowconfigure(2, pad=5)
        self.rowconfigure(3, pad=5)
        self.rowconfigure(4, pad=5)
        self.rowconfigure(5, pad=5)
        self.rowconfigure(6, pad=5)
        self.rowconfigure(7, pad=5)
        
        #LEFT TEXTBOX
        self.area = Text(self)
        self.area.grid(row=0, column=0, columnspan=1, rowspan=8, 
            padx=5, sticky=E+W+S+N)
        
        #RIGHT TEXTBOX
        self.area2 = Text(self)
        self.area2.grid(row=0, column=2, columnspan=1, rowspan=8, 
            padx=5, sticky=W+E+S+N)
        
        #SCORES/LABELS
        lbl = Label(self, text="Actual Score")
        lbl.grid(row=4, column=1, sticky=W, pady=4, padx=5)
        self.scorebox = Text(self, width=2, height=1)
        self.scorebox.grid(row=4, column=1, sticky=E)
        
        lbl2 = Label(self, text="Our Score")
        lbl2.grid(row=5, column=1, sticky=W, pady=4, padx=5)
        self.scorebox2 = Text(self, width=2, height=1)
        self.scorebox2.grid(row=5, column=1, sticky=E)
        
        lbl3 = Label(self, text="Sentiment")
        lbl3.grid(row=6, column=1, sticky=W)
        self.posneg = Text(self, width=3, height=1)
        self.posneg.grid(row=6, column=1, sticky=E)

        seedEntry = Entry(self)
        seedEntry.grid(row=7, column=1, sticky=W, pady=4, padx=5)
        seedBtn = Button(self, text='Gen w/ Seed', command=genSeed)
        seedBtn.grid(row=7, column=1, sticky=E)

        ###########
        #BUTTONS
        ###########
        #row 0
        trainNBBtn = Button(self, text="TrainClassifiers", command=mainInterface.trainNB)
        trainNBBtn.grid(row=0, column=1, sticky=N)
        #trainSVCBtn = Button(self, text="TrainSVC", command=mainInterface.trainSVC)
        #trainSVCBtn.grid(row=0, column=1, sticky=N+E)
        
        #row 1
        nbBtn = Button(self, text="NB", command=self.analyzeNB)
        nbBtn.grid(row=1, column=1, sticky=N+E)
        gbtn = Button(self, text="Generate", command=genRandom)
        gbtn.grid(row=1, column=1, sticky=N) 
        nltk_nb_btn = Button(self, text="NB_nltk", command=self.analyzeNB_nltk)
        nltk_nb_btn.grid(row=1, column=1, sticky=N+W)
        
        #row 2
        svcBtn = Button(self, text="SVM", command=self.analyzeSVC)
        svcBtn.grid(row=2, column=1, sticky=N+E)
        showStatsBtn = Button(self, text="Show Stats", command=self.showStats)
        showStatsBtn.grid(row=2, column=1, sticky=N)
        logReg = Button(self, text="LogReg", command=self.analyzeLogReg)
        logReg.grid(row=2, column=1, sticky=N+W)
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
        return text

    def showLoading(self):
        self.attemptedMarkov = True
        popup = Toplevel()
        text = Message(popup, text="The Markov Generator is still loading!\n\nText will show up when loaded!")
        text.pack()
        closePop = Button(popup, text="Okay!", command=popup.destroy)
        closePop.pack()  
         
    ######  
    ##Classifier Use Functions
    ######
    def analyzeNB(self):
        mainInterface.analyzeNB(self.area, self.posneg)
            
    def analyzeNB_nltk(self):
        mainInterface.analyzeNB_nltk(self.area, self.posneg)
        
    def analyzeSVC(self):
		mainInterface.analyzeSVC(self.area, self.posneg)

    def analyzeLogReg(self):
		mainInterface.analyzeLogReg(self.area, self.scorebox2)
		
    def showStats(self):
        mainInterface.showStats(self.area2)
		
    #End interface functions

def createUI(root):
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    
    
if __name__ == '__main__':
    createUI()
