from algorithms import Alignment
from pyDatalog import pyDatalog

# create some python functions as helpers, because pyDatalog allows this

# string length function
def strlen(x):
    if isinstance(x,basestring):
        return len(x)
    return 0

# character equality function
# this is a python function, so in true pythonic fashion, the comparison is very general
# here, we just mean to use it as character comparison
def match(a,b):
    return a==b

# Smith-Waterman wrapper
def sw_wrapper(a,b):
    print('{0} : {1}'.format(a,b))
    score = Alignment.SmithWaterman(a,b)
    print('score = {0}'.format(score))
    return score

# create required terms
# variables
pyDatalog.create_terms('X,Y,Z,LX,LY')
# data tables
pyDatalog.create_terms('seqs,cross_seqs,cross_seqs_lens,matches,seqlens,sw')
# python functions
pyDatalog.create_terms('strlen,match,sw_wrapper')

# assert some facts (i.e. add some sequences to the 'seqs' 'table')
sequences = ['ATA','ACGA','ATTCGAA','GGAGA','TTTACC','ACTGGAG','TGGACC']
for s in sequences:
    + seqs(s)

print('seqs')
print(seqs(X))

seqlens(X,Y) <= seqs(X) & (Y==strlen(X))
print(seqlens(X,Y))

# generate the cross product of seqs x seqs
# this could define all pairs of seqs we want to align (i.e. align X to Y)
# third condition in body prohibits (X,X) tuples
cross_seqs(X,Y) <= seqs(X) & seqs(Y) & (X!=Y)

print('cross_seqs')
print(cross_seqs(X,Y))

# generate alignment scores by calling out to a python function
# now, can we actually write the algorithm in pyDatalog syntax???
sw(X,Y,Z) <= cross_seqs(X,Y) & (Z==sw_wrapper(X,Y))
print('Smith-Waterman')
print(sw(X,Y,Z))

#sw(X,Y) <= cross_seqs(X,Y) & (Alignment.SmithWaterman(X,Y)>=0)
#print(sw(X,Y))

# generate lengths for each sequence in cross_seqs
cross_seqs_lens(X,Y,LX,LY) <= cross_seqs(X,Y) & (LX==strlen(X)) & (LY==strlen(Y))
print('cross_seqs_lens')
print(cross_seqs_lens(X,Y,LX,LY))

"""
# here, we "cheat" and just call out to our python match function to filter results
# for fun, let's get all the pairs (X,Y) from cross_seqs that have same first character
matches(X,Y) <= cross_seqs(X,Y) & (match(X[0],Y[0])==True)

print('matches')
print(matches(X,Y))

# so, let's try to define a function within pyDatalog syntax to do the same thing
pyDatalog.create_terms('match2,matches2')
(match2[X,Y] == True) <= (X==Y)
(match2[X,Y] == False) <= (X!=Y)
# this returns same as matches 'table' above, hooray!
matches2(X,Y) <= cross_seqs(X,Y) & (match2[X[0],Y[0]]==True)
print(matches2(X,Y))
"""

# create required terms
# variables
pyDatalog.create_terms('X,Y,Z,LX,LY,N')
# data tables
pyDatalog.create_terms('prefix,r,suffix,cc')
# python functions
pyDatalog.create_terms('strlen,match')

# assert some facts (i.e. add some sequences to the 'seqs' 'table')
sequences = ['ATACCAGAGAC','GACGA','ATTCGAC']
for s in sequences:
    + r(s)

# try to implement some sequence datalog stuff in pyDatalog -- see if stuff just works

# get all prefixes of all sequences in r(X)
prefix(X) <= r(X)
prefix(Z) <= prefix(X) & (N==strlen(X)) & (Z==X[0:N-1]) & (Z!='')
print('prefix')
print(prefix(X))

# concatenation
cc(Z) <= r(X) & r(Y) & (X!=Y) & (Z==(X+Y))
print('concatenation')
print(cc(Z))

# get all suffixes of all sequences in r(X)
suffix(X) <= r(X)
suffix(Z) <= suffix(X) & (Z==X[1:]) & (Z!='')
print('suffix')
print(suffix(X))

# seeds - extract all subsequences of length SL from sequences in r(X)
pyDatalog.create_terms('seeds,SL,temp')
temp(X) <= suffix(X) & (SL==5) & (strlen(X)>=SL)
print(temp(X))
seeds(Z) <= temp(X) & (SL==5) & (Z==X[0:SL])
print(seeds(Z))

# different implementation of all substrings (seeds) of length SL
# creates table of (Z,X) pairs where Z is original sequence and X is seed of length SL
pyDatalog.create_terms('newseeds,N1,N2')
newseeds(Z,N1,X) <= r(Z) & (SL==5) & (N1.in_(range_(strlen(Z)))) & (X==Z[N1:N1+SL]) & (strlen(X)>=SL)

print(newseeds(Z,N1,X))

pyDatalog.create_terms('lens')
lens(X,N) <= r(X) & (N==strlen(X))
print(lens(X,N))


def score(a,b):
    if a==b:
        return 0
    return 1

pyDatalog.create_terms('hamming,words,w,score,hammingscores,S,HS,K,hs')

w = ['hello','helps','world','worne']
for ww in w:
    + words(ww)

hammingscores(X,Y,K,S) <= words(X) & words(Y) & (K.in_(range_(strlen(X)))) & (strlen(X)==strlen(Y)) & (S==score(X[K],Y[K]))
print(hammingscores(X,Y,N,S))

# hamming distance function
(hs[X,Y]==sum_(S, for_each=N)) <= hammingscores(X,Y,N,S)

# query for a specific X,Y pair of words within hammingscores table
print(hs['hello','world']==Y)

# generate hamming distance for every X,Y pair in hammingscores table
hs(X,Y,HS) <= hammingscores(X,Y,N,S) & (HS==hs[X,Y])
print(hs(X,Y,HS))

"""
hammingscores(X,Y,K,S) <= words(X) & words(Y) & (K.in_(range_(strlen(X)))) & (strlen(X)==strlen(Y)) & (S==score(X[K],Y[K]))
print(hammingscores(X,Y,N,S))
cc(Z,N,S) <= hammingscores(X,Y,N,S) & (Z==X+Y)
print(cc(X,N,S))

hamming(X,HS) <= cc(X,N,S) & (HS==S)
print(hamming(X,HS))

(hs[X]==sum_(S, for_each=N)) <= cc(X,N,S)

print(hs['hellohelps']==Y)
"""
