from pyDatalog import pyDatalog

# create some python functions as helpers, because pyDatalog allows this

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

# create required terms
# variables
pyDatalog.create_terms('X,Y,Z,LX,LY')
# data tables
pyDatalog.create_terms('seqs,cross_seqs,cross_seqs_lens,matches,seqlens')
# python functions
pyDatalog.create_terms('strlen,match')

# assert some facts (i.e. add some sequences to the 'seqs' 'table')
sequences = ['ATA','ACGA','ATTCGAA','GGAGA','TTTACC','ACTGGAG','TGGACC']
for s in sequences:
    + seqs(s)

print('seqs')
print(seqs(X))

seqlens(X,Y) <= seqs(X) & (Y==strlen(X))
print(seqlens(X,Y))

# generate the cross product of seqs x seqs
# this could define all pairs of seqs we want to align (i.e. align X to Y)
# third condition in body prohibits (X,X) tuples
cross_seqs(X,Y) <= seqs(X) & seqs(Y) & (X!=Y)

print('cross_seqs')
print(cross_seqs(X,Y))

# generate lengths for each sequence in cross_seqs
cross_seqs_lens(X,Y,LX,LY) <= cross_seqs(X,Y) & (LX==strlen(X)) & (LY==strlen(Y))
print('cross_seqs_lens')
print(cross_seqs_lens(X,Y,LX,LY))

# here, we "cheat" and just call out to our python match function to filter results
# for fun, let's get all the pairs (X,Y) from cross_seqs that have same first character
matches(X,Y) <= cross_seqs(X,Y) & (match(X[0],Y[0])==True)

print('matches')
print(matches(X,Y))

# so, let's try to define a function within pyDatalog syntax to do the same thing
pyDatalog.create_terms('match2,matches2')
(match2[X,Y] == True) <= (X==Y)
(match2[X,Y] == False) <= (X!=Y)
# this returns same as matches 'table' above, hooray!
matches2(X,Y) <= cross_seqs(X,Y) & (match2[X[0],Y[0]]==True)
print(matches2(X,Y))
