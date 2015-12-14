import random

from pyDatalog import pyDatalog

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

pyDatalog.create_terms('strlen, match')

def rand_string_n(n):
    """
    Returns a random string of A,T,G,C characters of length n.
    """
    return ''.join([random.choice(['A','T','G','C']) for i in range(n)])
