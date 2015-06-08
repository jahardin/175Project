============================================================
INSTRUCTIONS ON RUNNING PROJECT
============================================================
Run main.py to bring up the interface.

In the interface there are 3 main components, the Right Textbox, the Left Textbox and the center control with the buttons. The left textbox is where the movie review's text will be processed. You can load reviews into the Left Textbox via the menu File>Open and then select a movie review from the "test" folder. Alternatively you can type in your own review or click the "Generate" button from the Center Control to generate a review. 

At the top of the Center Control are three button "TrainDT", "TrainNB" and "TrainMultiNB". Each of these trains their respective classifier "Decsion Tree", "Naive Bayes" and "Multinomial Naive Bayes". After training information concerning each classifier is saved to a text file. 

At the bottom of the center control there are buttons: "NB_nltk", "DT_nltk", "SVC_nltk" which each analyze the text in the Left Textbox according to their respective classifiers and assigns a "Positive or "Negative" sentiment to the text. 

============================================================
THE DIFFERENT FILES
============================================================
DecisionTreeModel.py - 



============================================================
LIBRARY CODE USED
============================================================




============================================================
HANDWRITTEN CODE
============================================================



============================================================
LIBRARIES NEED
============================================================
NumPy - http://www.numpy.org/
Pandas - http://pandas.pydata.org/
Scikit-learn - http://scikit-learn.org/stable/
nltk - http://www.nltk.org/
tkinter - https://wiki.python.org/moin/TkInter
