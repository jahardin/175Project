from Tkinter import Tk, Text, BOTH, Menu, W, N, E, S, INSERT, END
import os, random
from ttk import Frame, Button, Label, Style
import tkFileDialog
from tkFileDialog import askopenfilename
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from KaggleWord2VecUtility import KaggleWord2VecUtility
import pandas as pd
import numpy as np



class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        self.trainAI()
        
    def trainAI(self):
        train = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'labeledTrainData.tsv'), header=0, delimiter="\t", quoting=3)
        test = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'testData.tsv'), header=0, delimiter="\t", quoting=3 )
        
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
        
        self.parent.title("Windows")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        #ROWS/COLUMNS
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, pad=5)
        self.columnconfigure(2, pad=50)
        self.columnconfigure(3, pad=5)
        self.columnconfigure(4, pad=5)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, pad=5)
        self.rowconfigure(3, pad=5)
        self.rowconfigure(4, pad=5)
        
        #LEFT TEXTBOX
        self.area = Text(self)
        self.area.grid(row=0, column=0, columnspan=1, rowspan=5, 
            padx=5, sticky=E+W+S+N)
        
        #RIGHT TEXTBOX
        self.area2 = Text(self)
        self.area2.grid(row=0, column=3, columnspan=1, rowspan=5, 
            padx=5, sticky=E+W+S+N)
            
        #SCORES/LABELS
        lbl = Label(self, text="Actual Score")
        lbl.grid(row=3, column=2, sticky=W, pady=4, padx=5)
        self.scorebox = Text(self, width=2, height=1)
        self.scorebox.grid(row=3, column=2, sticky=E)
        lbl2 = Label(self, text="Our Score")
        lbl2.grid(row=4, column=2, sticky=W, pady=4, padx=5)
        self.scorebox2 = Text(self, width=2, height=1)
        self.scorebox2.grid(row=4, column=2, sticky=E)
        
        #BUTTONS
        abtn = Button(self, text="Analyze")
        abtn.grid(row=0, column=2, sticky=N)
        gbtn = Button(self, text="Generate")
        gbtn.grid(row=1, column=2, sticky=N) 
        ggbtn = Button(self, text="Random", command=giveRandom)
        ggbtn.grid(row=2, column=2, sticky=N)

    def onOpen(self):
        ftypes = [('Text Files', '*.txt'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()

        if fl != '':
            text = self.readFile(fl)
            self.area.insert(END, text)

    def readFile(self, filename):
        f = open(filename, "r")
        text = f.read()
        filenamearr = filename.split("_")
        score = filenamearr[1].split(".")
        self.scorebox.insert(INSERT, score[0])
        print "score " + score[0]
        return text
        
    
        
              

def main():
  
    root = Tk()
    root.geometry("350x300+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()