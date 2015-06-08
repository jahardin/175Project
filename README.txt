============================================================
INSTRUCTIONS ON RUNNING PROJECT
============================================================
Run main.py to bring up the interface.

In the interface there are 3 main components, the Right Textbox, the Left Textbox and the center control with the buttons. The left textbox is where the movie review's text will be processed. You can load reviews into the Left Textbox via the menu File>Open and then select a movie review from the "test" folder. Alternatively you can type in your own review or click the "Generate" button from the Center Control to generate a review. 

At the top of the Center Control are three button "TrainDT", "TrainNB" and "TrainMultiNB". Each of these trains their respective classifier "Decsion Tree", "Naive Bayes" and "Multinomial Naive Bayes". After training information concerning each classifier is saved to a text file. 

At the bottom of the center control there are buttons: "NB_nltk", "DT_nltk", "SVC_nltk" which each analyze the text in the Left Textbox according to their respective classifiers and assigns a "Positive or "Negative" sentiment to the text. 

The "LogReg" button analyzes the text in the Left Textbox using Logical Regressing and assigns a score value 1 thru 10.

The "Show Stats" button button loads a comparasion of the classifiers into the Right Textbox.

At the bottom of the Center Control is "Actual Score". When you load a test review via File>Open the score for that review will be loaded into this box.

At the bottom of the Center Control is "Our Score". When you run any classifier to analyze the sentiment of the Left Textbox our Positive or Negative score given will appear here. 

At the bottom of the Center Control is an input box and button "Gen w/ Seed".
The input box takes a two word seed and generates a review using this seed into the Left Textbox.


============================================================
THE DIFFERENT FILES
============================================================
combinedNeg - every negative review from the training corpus 
combinedPos - every positive review from the training corpus
DecisionTreeModel.py - Holds the model for the Decision tree classifier. nltk library used
GenMarkov.py - Holds the code for the Markov Model text generation. Handwritten
imdb.vocab - Holds the structured vocabularty used by the Logical Regression
_init_.py - needed for Python
interface.py - Holds code for the interface and interacting with it. Handwritten
logicalRegression.py - Holds  code for the Logical Regression analysis. Handwritten
logRegScale.txt - word weights used by the Logical Regression model
logRegVocab.txt - structured vocabulary for the Logical Regression model
logRegWeights.txt - weights for the Logical Regression model
main.py - The main file of the program. Brings everything together. Handwritten
maxEntModel - Maximum Entropy model for analysis. Unfinished, nltk library used
multinomialNBModel.py - Holds the model for the multinomial Naive Bayes classifier. nltk library used
naiveBayes.py - Holds code for the basic naive bayes model. nltk library used
naiveBayes.m - Hold code for Matlab naive bayes, soon to be implemented in python. Handwritten
naiveBayes2.py - training file
nbHand.py - currently holds an nltk implementation of the naive bayes classifier, will be handwritten before final. nltk/handwritten
statsRecordNB.txt - holds recorded classifier performance data
svcModel.py - holds the SVC Model for classifier. nltk
test.py - current test visualation comparasion. handwritten

175FinalReport - The final report for the class

FOLDERS
-----------
test - contains 


.pickle files
-------------
All .pickle files hold saved classifer model according to their respective names 


============================================================
LIBRARY CODE USED
============================================================
NLTK
Scikit-learn
Tkinter
Pandas
NumPy
MatplotLib



============================================================
HANDWRITTEN CODE
============================================================
naiveBayes.m
main.py
interface.py
logicalRegression.py
GenMarkov.py


============================================================
LIBRARIES NEED
============================================================
NumPy - http://www.numpy.org/
Pandas - http://pandas.pydata.org/
Scikit-learn - http://scikit-learn.org/stable/
nltk - http://www.nltk.org/
tkinter - https://wiki.python.org/moin/TkInter
matplotlib - http://matplotlib.org/

============================================================
STILL TO DO
============================================================
pythonize the handwritten naive bayes. Get the last classifiers working and the comparisons finished in visualizing as well as appearing in the Right Textbox
