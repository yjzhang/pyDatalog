import random
import time

from pyDatalog import pyDatalog
from sequence_datalog_base import *

alphabet = ['A','T','G','C','N']

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

# citation: http://cs.union.edu/~striegnk/courses/nlp-with-prolog/html/node5.html
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

# TODO: not working
def build_sw_fsm(s, n, costs):
    """
    Builds a Smith-Waterman FSM where n is the maximum Smith-Waterman
    distance between s and a given string
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
                # local alignment - going back to zero
                +arc((i,e),(i+1,0),'*')
    for e in range(n+1):
        if e<n:
            +arc((len(s),e),(len(s),e+1),'*')
        +final((len(s),e))

pyDatalog.create_terms('dfa_recognize, dfa_init, dfa_arc, dfa_final,X,Y')
dfa_recognize(N,'') <= dfa_final(N)
dfa_recognize(N1,S) <= (dfa_arc(N1,N2,S[0]) & dfa_recognize(N2,S[1:]))
# dfas are more efficient because they do not have non-determinism or null
# transitions
#dfa_recognize(N1,S) <= (dfa_arc(N1,N2,'#') & dfa_recognize(N2,S))
#dfa_recognize(N1,S) <= (dfa_arc(N1,N2,'*') & dfa_recognize(N2,S[1:]))

# citation (same author as the one to build_fsm): 
# https://gist.github.com/Arachnid/491973
def convert_to_dfa(start_node):
    +dfa_arc(0,1,'t')
    """
    Converts the nfsm starting from the given node to a deterministic fsm.
    This runs the powerset construction algorithm.
    """
    +dfa_init((start_node,))
    to_visit = [(start_node,)]
    visited = set()
    n_alphabet = alphabet + ['#','*']
    while to_visit:
        current_node = to_visit.pop()
        next = arc(current_node, X, Y)
        for action in n_alphabet:
            if action=='#':
                continue
            next = (X.in_((current_node)) & arc(X, Y, action))
            if not next:
                continue
            new_state = tuple(sorted(n[1] for n in next))
            if new_state not in visited:
                to_visit.append(new_state)
                visited.add(new_state)
                if (X._in(new_state) & final(X)):
                    +dfa_final(new_state)
            # set a "default" action to go to the next state
            if action=='*':
                for a in alphabet:
                    if not dfa_arc(current_node, X, a):
                        #pass
                        +dfa_arc(current_node, new_state, a)
            else:
                # this part shouldn't execute if things go well?
                for old_node in dfa_arc(current_node, X, action):
                    print('losing...')
                    -dfa_arc(current_node, old_node, action)
                +dfa_arc(current_node, new_state, action)

def test(n,k):
    s = ''.join([random.choice(['A','T','G','C']) for i in range(n)])
    t = time.time()
    build_fsm(s, k)
    #print('Time to construct nfa: {0}'.format(time.time() - t))
    t0 = time.time() - t
    t = time.time()
    convert_to_dfa((0,0))
    #print('Time to convert to dfa: {0}'.format(time.time() - t))
    t1 = time.time() - t
    return s, t0, t1

def rand_change_k(s, k):
    l = list(s)
    for i in range(k):
        ind = random.randint(0,len(l)-1)
        l[ind] = 'N'
    return ''.join(l)

if __name__ == '__main__':
    import sys
    del initial, final, arc
    del dfa_init, dfa_arc, dfa_final
    string_size = int(sys.argv[1])
    max_errors = int(sys.argv[2])
    num_errors = int(sys.argv[3])
    pyDatalog.create_terms('initial,final,arc')
    pyDatalog.create_terms('dfa_recognize, dfa_init, dfa_arc, dfa_final,X,Y')
    s, t0, t1 = test(string_size,max_errors)
    t = time.time()
    print >> sys.stderr, ((N==((0,0),)) & (S==s) & dfa_recognize(N,S))
    t2 = time.time() - t
    #print('Time for dfa exact match: {0}'.format(t2))
    t = time.time()
    print >> sys.stderr, ((N==((0,0),)) & (S==rand_change_k(s,num_errors)) & dfa_recognize(N,S))
    t3 = time.time() - t
    #print('Time for dfa match with 3 misses: {0}'.format(t3))
    t = time.time()
    print >> sys.stderr, ((N==((0,0))) & (S==rand_change_k(s,num_errors)) & recognize1(N,S))
    t4 = time.time() - t
    #print('Time for nfa match with 3 misses: {0}'.format(t4))
    # testing for non-deterministic connections in dfa
    print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}'.format(string_size,
        max_errors,num_errors,t0,t1,t2,t3,t4))
