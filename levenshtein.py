import sys
import time
import random
from algorithms import Alignment

def rand_change_k(s, k):
    l = list(s)
    for i in range(k):
        ind = random.randint(0,len(l)-1)
        l[ind] = 'N'
    return ''.join(l)

def exp(l,k):
    alphabet = ['A','T','C','G']
    a = ''.join([random.choice(alphabet) for i in xrange(l)])
    b = rand_change_k(a,k)

    # perform experiment in native python
    t = time.time()
    res = Alignment.Levenshtein(a,b)
    #print(res)
    pyTime = time.time() - t
    #print('Time in native python: {0}'.format(pyTime))

    return pyTime, res

def usage():
    print('python hamming.py')
    sys.exit(-1)

if __name__ == '__main__':
    if len(sys.argv) != 1:
        usage()
    ll = [10,20,40,80,160,320]
    for l in ll:
        for k in range(3,10):
            print('{0},{1},{2}'.format(l,k,exp(l,k)[0]))
