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

pyDatalog.create_terms('seeds,r,strlen,ss,Z,X,Y,N,SL,W')

def build(args):
    ref = args[0]
    query = args[1]
    sl = len(query)

    # different implementation of all substrings (seeds) of length SL
    # creates table of (Z,X) pairs where Z is original sequence and X is seed of length SL
    + r(ref)
    #seeds(Z,N,X) <= r(Z) & (SL==sl) & (N.in_(range_(strlen(Z)))) & (X==Z[N:N+SL]) & (strlen(X)==SL)
    #print(seeds(Z,N,X))
    seeds(Z,X) <= r(Z) & (SL==sl) & (N.in_(range_(strlen(Z)))) & (X==Z[N:N+SL]) & (strlen(X)==SL)
    #print(seeds(Z,X))

def ask(q):
    # seeds query function
    (ss[Y]==X) <= seeds(Z,X) & (Y==X) & (W==X)
    print(ss[q]==X)

def exp(rl,ql):
    # generate our random reference sequence, and extract a query sequence from it
    alphabet = ['A','T','C','G']
    ref = ''.join([random.choice(alphabet) for i in xrange(rl)])
    # pick random index from 0 to rl-ql, and select substring of a[i:i+ql]
    i = random.randint(0,rl-ql)
    query = ref[i:i+ql]

    # perform experiment in pyDatalog
    t = time.time()
    build([ref,query])
    ask(query)
    pyDatalogTime = time.time() - t
    print('Time in pyDatalog: {0}'.format(pyDatalogTime))

    # perform experiment in native python
    t = time.time()
    res = Alignment.ExactMatch(ref,query)
    print(res)
    pyTime = time.time() - t
    print('Time in native python: {0}'.format(pyTime))

    return pyDatalogTime, pyTime

def usage():
    print('python hamming.py <ref length> <query length>')
    sys.exit(-1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    exp(int(sys.argv[1]), int(sys.argv[2]))
