import random
import time

from pyDatalog import pyDatalog
from sequence_datalog_base import *

# 1. testing fsm
pyDatalog.create_terms('initial,final,arc')

+initial(1)
+final(4)
+arc(1,2,'h')
+arc(2,3,'a')
+arc(3,4,'!')
+arc(3,1,'#')

pyDatalog.create_terms('recognize1, traverse1, N, N1, N2, S, S1, S2')

# the '#' symbol matches the empty character.
# the '*' symbol matches any character.

# citation: http://cs.union.edu/~striegnk/courses/nlp-with-prolog/html/node5.html#l1.prolog
# this allows for the construction of nondeterministic fsms
recognize1(N,'') <= final(N)
recognize1(N1,S) <= (arc(N1,N2,S[0]) & recognize1(N2,S[1:]))
recognize1(N1,S) <= (arc(N1,N2,'#') & recognize1(N2,S))
recognize1(N1,S) <= (arc(N1,N2,'*') & recognize1(N2,S[1:]))

# this works!!!

# building a levenshtein automaton for a given string - this construct 

# citation: http://blog.notdot.net/2010/07/Damn-Cool-Algorithms-Levenshtein-Automata
def build_fsm(s, n):
    """
    Constructs a Levenshtein automaton for the given string s, where
    n is the maximum levenshtein distance.
    """
    +initial((0,0))
    for i, c in enumerate(s):
        for e in range(n+1):
            # match
            +arc((i,e), (i+1,e), c)
            if e < n:
                # deleteion
                +arc((i,e),(i,e+1),'*')
                # insertion
                +arc((i,e),(i+1,e+1),'#')
                # substitution
                +arc((i,e),(i+1,e+1),'*')
    for e in range(n+1):
        if e<n:
            +arc((len(s),e),(len(s),e+1),'*')
        +final((len(s),e))

# citation: https://gist.github.com/Arachnid/491973
pyDatalog.create_terms('dfa_recognize, dfa_init, dfa_arc, dfa_final,X,Y')
dfa_recognize(N,'') <= dfa_final(N)
dfa_recognize(N1,S) <= (dfa_arc(N1,N2,S[0]) & dfa_recognize(N2,S[1:]))
dfa_recognize(N1,S) <= (dfa_arc(N1,N2,'#') & dfa_recognize(N2,S))
dfa_recognize(N1,S) <= (dfa_arc(N1,N2,'*') & dfa_recognize(N2,S[1:]))

def convert_to_dfa(start_node):
    """
    Converts the nfsm starting from the given node to a deterministic fsm.
    """
    +dfa_init(start_node)
    to_visit = [start_node]
    visited = set()
    while to_visit:
        current_node = to_visit.pop()
        next = arc(current_node, X, Y)
        for n in next:
            if n[1]=='#':
                continue
            new_state = n[0]
            if new_state not in visited:
                to_visit.append(new_state)
                visited.add(new_state)
                if final(new_state):
                    +dfa_final(new_state)
            if n[1]=='*':
                +dfa_arc(current_node, new_state, '*')
            else:
                +dfa_arc(current_node, new_state, n[1])

def test():
    s = ''.join([random.choice(['A','T','G','C']) for i in range(500)])
    build_fsm(s, 10)
    convert_to_dfa((0,0))
    return s

def rand_permute_k(s, k):
    l = list(s)
    for i in range(k):
        ind = random.randint(0,len(l)-1)
        l[ind] = 'K'
    return ''.join(l)

if __name__ == '__main__':
    s = test()
    t = time.time()
    print((N==(0,0)) & (S==s) & dfa_recognize(N,S))
    print('Time for dfa exact match: {0}'.format(time.time() - t))
    t = time.time()
    print((N==(0,0)) & (S==rand_permute_k(s,3)) & dfa_recognize(N,S))
    print('Time for dfa match with 3 misses: {0}'.format(time.time() - t))
    t = time.time()
    print((N==(0,0)) & (S==rand_permute_k(s,3)) & recognize1(N,S))
    print('Time for nfa match with 3 misses: {0}'.format(time.time() - t))
