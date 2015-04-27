from Tkinter import Tk, Text, BOTH, Menu, W, N, E, S, INSERT, END, Message, Toplevel
import os, random
from ttk import Frame, Button, Label, Style
import tkFileDialog
from tkFileDialog import askopenfilename
import threading


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
            self.area2.delete(1.0, END)
            self.area2.insert(1.0, self.markovGenerator.GenRandom())

    def initUI(self):

        #BUTTON CALLBACKS
        def giveRandom():
            print random.choice(os.listdir("C:\\test\neg"))

        def genRandom():
            if not self.markovStarting:
                self.area2.delete(1.0, END)
                self.area2.insert(1.0, self.markovGenerator.GenRandom())
            else:
                self.showLoading()

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
        self.columnconfigure(0, weight=1, minsize=400)
        self.columnconfigure(1, pad=5)
        self.columnconfigure(2, pad=50)
        self.columnconfigure(3, weight=1, pad=5, minsize=400)
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
        gbtn = Button(self, text="Generate", command=genRandom)
        gbtn.grid(row=1, column=2, sticky=N)
        ggbtn = Button(self, text="Random", command=giveRandom)
        ggbtn.grid(row=2, column=2, sticky=N)

        self.parent.update()

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

    def showLoading(self):
        self.attemptedMarkov = True
        popup = Toplevel()
        text = Message(popup, text="The Markov Generator is still loading!\n\nText will show up when loaded!")
        text.pack()
        closePop = Button(popup, text="Okay!", command=popup.destroy)
        closePop.pack()

def main():

    root = Tk()
    root.geometry("1000x600+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()