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
recognize1(N,'') <= final(N)
recognize1(N1,S) <= (arc(N1,N2,S[0]) & recognize1(N2,S[1:]))
recognize1(N1,S) <= (arc(N1,N2,'#') & recognize1(N2,S))
recognize1(N1,S) <= (arc(N1,N2,'*') & recognize1(N2,S[1:]))

# this works!!!

# building a levenshtein automaton for a given string

# TODO: how to make these transitions work
pyDatalog.create_terms('s_any,s_null')

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
            +arc((len(s),e),(len(s),e+1),s_any)
        +final((len(s),e))
