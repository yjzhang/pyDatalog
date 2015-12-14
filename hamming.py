import sys
import time
import random
from algorithms import Alignment
from pyDatalog import pyDatalog

# create some python functions as helpers, because pyDatalog allows this

# string length function
def strlen(x):
    if isinstance(x,basestring):
        return len(x)
    return 0

# create required terms
# variables
pyDatalog.create_terms('X,Y,Z,LX,LY,N')

def score(a,b):
    if a==b:
        return 0
    return 1

pyDatalog.create_terms('hamming,words,w,score,hammingscores,S,HS,K,hs,strlen')

#w = ['hello','helps','world','worne']
def build(args):
    w = args
    for ww in w:
        + words(ww)

    hammingscores(X,Y,K,S) <= words(X) & words(Y) & (K.in_(range_(strlen(X)))) & (strlen(X)==strlen(Y)) & (S==score(X[K],Y[K]))
    #print(hammingscores(X,Y,N,S))
    
    # hamming distance function
    #(hs[X,Y]==sum_(S, for_each=N)) <= hammingscores(X,Y,N,S)

    # query for a specific X,Y pair of words within hammingscores table
    #print(hs['hello','world']==Y)

    # generate hamming distance for every X,Y pair in hammingscores table
    #hs(X,Y,HS) <= hammingscores(X,Y,N,S) & (HS==hs[X,Y])
    #print(hs(X,Y,HS))

def ask(a,b):
    # hamming distance function
    (hs[X,Y]==sum_(S, for_each=N)) <= hammingscores(X,Y,N,S)
    print(hs[a,b]==S)

def exp(l):
    alphabet = ['A','T','C','G']
    a = ''.join([random.choice(alphabet) for i in xrange(l)])
    b = ''.join([random.choice(alphabet) for i in xrange(l)])

    # perform experiment in pyDatalog
    t = time.time()
    build([a,b])
    ask(a,b)
    pyDatalogTime = time.time() - t
    print('Time in pyDatalog: {0}'.format(pyDatalogTime))

    # perform experiment in native python
    t = time.time()
    res = Alignment.Hamming(a,b)
    print(res)
    pyTime = time.time() - t
    print('Time in native python: {0}'.format(pyTime))

    return pyDatalogTime, pyTime

def usage():
    print('python hamming.py <sequence length>')
    sys.exit(-1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    exp(int(sys.argv[1]))
