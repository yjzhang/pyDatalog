import sys
from algorithms import Alignment

def lev(a,b):
    print('{0}, {1}, {2}'.format(a,b,Alignment.Levenshtein(a,b)))

if __name__ == '__main__':
    lev(sys.argv[1],sys.argv[2])
