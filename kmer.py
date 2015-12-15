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

pyDatalog.clear()
pyDatalog.create_terms('seedsa,seedsb,r,s,strlen,X,Y,Z,res,A,B,SL,N')

def build(a,b,k):
    # creates table of (Z,X) pairs where Z is original sequence and X is seed (kmer) of length SL
    + r(a)
    seedsa(Z,X) <= r(Z) & (SL==k) & (N.in_(range_(strlen(Z)))) & (X==Z[N:N+SL]) & (strlen(X)==SL)
    #print(seedsa(Z,X))
    + s(b)
    seedsb(Z,X) <= s(Z) & (SL==k) & (N.in_(range_(strlen(Z)))) & (X==Z[N:N+SL]) & (strlen(X)==SL)
    #print(seedsb(Z,X))

def ask():
    # seeds query function
    res(X) <= seedsa(A,Y) & seedsb(B,Z) & (Z==Y) & (X==Z)
    #print(res(X))
    print(len_(res(X))==Y)

def exp(args):
    # generate two random sequences
    l = int(args[0])
    k = int(args[1])
    alphabet = ['A','T','C','G']
    a = ''.join([random.choice(alphabet) for i in xrange(l)])
    b = ''.join([random.choice(alphabet) for i in xrange(l)])

    # perform experiment in pyDatalog
    t = time.time()
    build(a,b,k)
    ask()
    pyDatalogTime = time.time() - t
    print('Time in pyDatalog: {0}'.format(pyDatalogTime))

    # perform experiment in native python
    t = time.time()
    res = Alignment.KmerMatch(a,b,k)
    print(res)
    pyTime = time.time() - t
    print('Time in native python: {0}'.format(pyTime))

    return pyDatalogTime, pyTime

def usage():
    print('python hamming.py <seq length> <k>')
    sys.exit(-1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    res = exp(sys.argv[1:])
    print('{0},{1},{2},{3}'.format(int(sys.argv[1]),int(sys.argv[2]),res[0],res[1]))
