import nltk
import random
from nltk.grammar import is_nonterminal
from nltk import Nonterminal, nonterminals, Production, CFG, induce_pcfg
from nltk.corpus import treebank

grammar = nltk.PCFG.fromstring("""
    S  -> NP VP     [1.0]
    NP -> Det Nom   [0.6]
    NP -> PropN     [.4]
    Nom -> Adj Nom  [.2]
    Nom -> N        [.8]
    VP -> V Adj     [.4]
    VP -> V NP      [.2]
    VP -> V S       [.1]
    VP -> V NP PP   [.3]
    PP -> P NP      [1.0]
    PropN -> 'Samuel L. Jackson' [0.25]
    PropN -> 'Uma Thurman' [0.25]
    PropN -> 'John Travolta' [0.3]
	PropN -> 'Quentin Tarantino' [0.1]
	PropN -> 'Pulp Fiction' [0.1]
    Det -> 'the' [0.5]
    Det -> 'a' [0.3]
	Det -> 'an' [0.2]
    N -> 'film' [0.3]
    N -> 'movie' [0.1]
    N -> 'action' [0.2]
    N -> 'excitement' [0.2]
    N -> 'filmography' [0.2]
    Adj  -> 'terrific' [0.25] 
    Adj -> 'fantastic' [0.25]
    Adj -> 'well' [0.25]
    Adj -> 'exciting' [0.25]
    V -> 'featured' [0.25]
    V -> 'had' [0.2]
    V -> 'said' [0.1]
    V -> 'thought' [0.05]
    V -> 'was' [0.2]
    V -> 'put' [0.2]
    P -> 'on' [1.0]
    """)

print 'A PCFG grammar:', repr(grammar)
print '    grammar.start()       =>', repr(grammar.start())
print '    grammar.productions() =>',
# Use .replace(...) is to line-wrap the output.
print repr(grammar.productions()).replace(',', ',\n'+' '*29)


def sample_pcfg(grammar):
	# Sample a random sentence from a PCFG
	sent = [grammar.start()]
	while (  any([is_nonterminal(t) for t in sent]) ): # any symbol is a nonterminal
		# grab the first non-terminal and its productions
		t = next(t for t in sent if is_nonterminal(t))
		
		#print "sampling:", repr(t)
		
		prods = grammar.productions(lhs = t)
		
		#print "productions found:", repr(prods)
		
		# sample its realization
		r = random.random();
		i = -1
		while (r >= 0):
			i = i+1
			# print(prods[i].prob())
			r = r - prods[i].prob()
		
		# print "production chosen:", prods[i].rhs()
		
		j = sent.index(t)
		sent.remove(t)
		for rhs in prods[i].rhs():
			sent.insert(j,  rhs) 
			j = j+1
		# print "current sentence:", sent
	return sent



"""
# extract productions from three trees and induce the PCFG
print("Induce PCFG grammar from treebank data:")

productions = []
item = treebank._fileids[0]
for tree in treebank.parsed_sents(item)[:3]:
    # perform optional tree transformations, e.g.:
    tree.collapse_unary(collapsePOS = False)
    tree.chomsky_normal_form(horzMarkov = 2)
    productions += tree.productions()

S = Nonterminal('S')
grammar = induce_pcfg(S, productions)
"""

print(grammar)

for i in range(10):
	sent = sample_pcfg(grammar)
	str = ' '.join(sent)
	print str

