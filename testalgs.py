import sys
from algorithms import Alignment

def lev(a,b):
    print('{0}, {1}, {2}'.format(a,b,Alignment.Levenshtein(a,b)))

def kmers(a,b,k):
    print('{0}, {1}, {2}\n{3}'.format(a,b,k,Alignment.KmerMatch(a,b,k)))

if __name__ == '__main__':
    lev(sys.argv[1],sys.argv[2])
    kmers(sys.argv[1],sys.argv[2],sys.argv[3])
