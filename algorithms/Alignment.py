import pprint
import sys
import re

"""
Alignment: this module provides some basic sequence alignment functions.

Algorithms implemented:
1. Local alignment, Smith-Waterman
2. Exact search
3. kmer (substring) matching
4. Levenshtein distance
5. Hamming distance
"""

# exact search
def ExactMatch(a,b):
    """
    Search for string b in string a
    
    Return True if b is a substring of a
    """
    return True if a.find(b) >= 0 else False

# kmer (substring) matching
def getKmers(sequence, k):
    """
    Returns list of the kmers (in original sequence order) in the provided sequence
    Sequence length must be >= k, otherwise empty list is returned
    """
    k = int(k)
    if len(sequence) >= k :
        l = [ ''.join(sequence[i:i+k]) for i in xrange(len(sequence)-k+1) ]
        return l
    return list()

def KmerMatch(a,b,k):
    """
    Compare two strings based on 'kmers'

    Returns the number of unique kmers that matched
    """
    amers = getKmers(a,k)
    bmers = getKmers(b,k)

    matches = list(set(amers) & set(bmers))
    #print(matches)
    #print(len(matches))
    if matches:
        return len(matches)
    return 0

# Levenshtein distance
def Levenshtein(a,b):
    """
    naive Levenshtein distance function
    """
    m = len(a)
    n = len(b)

    # init scores matrix (m+1)*(n+1)
    scores = [[0 for x in xrange(n+1)] for x in xrange(m+1)]
    for i in xrange(1,m+1):
        scores[i][0] = i
    for j in xrange(1,n+1):
        scores[0][j] = j

    for j in xrange(0,n):    
        jj = j+1
        for i in xrange(0,m):
            ii = i+1
            if a[i] == b[j]:
                scores[ii][jj] = scores[ii-1][jj-1] # match
            else:
                scores[ii][jj] = min(scores[ii-1][jj]+1, # deletion
                                     scores[ii][jj-1]+1, # insertion
                                     scores[ii-1][jj-1]+1) # substitution

    return scores[m][n]

def accept_Levenshtein(a,b,n):
    """
    Returns True if Levenshtein(a,b) is in [0,n], i.e. within n
    """
    s = Levenshtein(a,b)
    return True if s >= 0 and s <= n else False

# Hamming distance
def Hamming(a,b):
    """
    naive Hamming distance computation

    returns -1 if length mismatch
    """
    if len(a) != len(b):
        # what to return for mismatched lengths?
        return -1 #max(len(a),len(b))
    diffs = 0
    for c1,c2 in zip(a,b):
        if c1 != c2:
            diffs += 1
    return diffs

def accept_Hamming(a,b,n):
    """
    Returns True if Hamming(a,b) is in [0,n], i.e. within n
    """
    s = Hamming(a,b)
    return True if s >= 0 and s <= n else False

# Smith-Waterman alignment scoring parameters
default_swparams = {
    "match" : 2, # bases match and are not N or -
    "mismatch" : -1, # bases do not match

    # unsure if these params are useful, or what they should be relative to match/mismatch
    "N" : 0, # N to any
    "purine" : 1, # purine match
    "pyrimidine" : 1, # pyrimidine match
}

def stringFormatAndLength(s):
    return "-"+s.upper(),len(s)+1

# base comparison scoring function
def score(a,b,params):
    if a == 'N' or b == 'N':
        # unknown base match
        return params["N"]
    elif (a == 'R' and (b == 'A' or b == 'G' or b == 'R')) or ((a == 'A' or a == 'G' or a == 'R') and b == 'R'):
        # purine match
        return params["purine"]
    elif (a == 'Y' and (b == 'C' or b == 'T' or b == 'Y')) or ((a == 'C' or a == 'T' or a == 'Y') and b == 'Y'):
        # pyrimidine match
        return params["pyrimidine"]
    elif a == b:
        # match
        return params['match']
    else:
        # mismatch
        return params['mismatch']

def printSwMatrix(a,b,scores):
    print(' '),
    for c in a:
        print('{0:>4s}'.format(c)),
    print
    for i in xrange(len(b)):
        print('{0}'.format(b[i])),
        for s in scores[i]:
            print('{0:>4d}'.format(s)),
        print
        #print (b[i] + ' ' + ' '.join([str(x) for x in scores[i]]))

def normalizeSwDistance(lenA,lenB,score):
    """
    Return a "normalized" distance score for local alignment

    The returned distance is in [0.0,1.0], where 1.0 means the local alignment was perfect
    - lenA and lenB are length of sequences without prepended '-' character

    TODO: determine correct way to normalize and compare scores such that distance score
    is statistically significant
    """
    # length of nucleotide sequences
    l = max(lenA,lenB)
    return float(score)/(float(l*params["match"]))

def SmithWaterman(a,b,swparams=default_swparams, debug=False):
    """
    Simple implementation of standard Smith-Waterman local alignment routine

    Computes optimal local alignment using parameters from swparams, in O(lenA*lenB) space
    and O(lenA*lenB) time.

    Inputs:
    a,b: input sequences; must only contain characters from {A,C,G,T,N,R,Y}
    swparams: alignment parameter dictionary

    Assumptions:
    1. sequence input contains only valid characters
    2. gaps in sequences are specified using N, where the gap length is the number of N's
    """
    
    # print input sequences
    if debug:
        print('input A: {0}'.format(a))
        print('input B: {0}'.format(b))

    # format strings, prepending '-' character to each sequence
    (a,lenA) = stringFormatAndLength(a)
    (b,lenB) = stringFormatAndLength(b)

    # initialize alignment score matrix
    # numRows = lenB
    # numCols = lenA
    # sequence A is along top, sequence B is along left, both start top left, work right (A) and down (B)
    scores = [[0 for x in xrange(lenA)] for x in xrange(lenB)]
    
    # fill rest of matrix
    for ib in xrange(1,lenB):
        for ia in xrange(1,lenA):
            # TODO: gap scoring scheme, i.e. for deletion/insertion do we penalize gap start same as extension?
            # deletion
            scoreLeft = scores[ib][ia-1] - 1
            # insertion
            scoreUp = scores[ib-1][ia] - 1
            # match/mismatch
            scoreDiag = scores[ib-1][ia-1] + score(a[ia],b[ib],swparams)
            # pick max of (0, left, up, diag)
            scores[ib][ia] = max(0,max(scoreLeft,max(scoreUp,scoreDiag)))

    # print scoring matrix
    printSwMatrix(a,b,scores)

    # compute aligned sequences
    maxIdx = (lenB-1,lenA-1) # (row,col)
    for ib in xrange(lenB-1,-1,-1):
        for ia in xrange(lenA-1,-1,-1):
            if scores[ib][ia] > scores[maxIdx[0]][maxIdx[1]]:
                maxIdx = (ib,ia)

    maxPath = [maxIdx]
    (maxScore,ib,ia) = (scores[maxIdx[0]][maxIdx[1]],maxIdx[0],maxIdx[1])
    if debug:
        print("Maximum score = " + str(maxScore))
    alignmentScore = maxScore
    while True:
        scoreLeft = scores[ib][ia-1] if ib >= 0 and ia-1 >= 0 else -1
        scoreUp = scores[ib-1][ia] if ib-1 >= 0 and ia >= 0 else -1
        scoreDiag = scores[ib-1][ia-1] if ib-1 >= 0 and ia-1 >= 0 else -1
        # choose between diag and left, favor diag
        (maxScore1,ib1,ia1) = (scoreDiag,ib-1,ia-1) if scoreDiag >= scoreLeft else (scoreLeft,ib,ia-1)
        # choose between previous max and up, favor previous
        (maxScore,ib,ia) = (maxScore1,ib1,ia1) if maxScore1 >= scoreUp else (scoreUp,ib-1,ia)
        # append to list
        maxPath.append((ib,ia))
        if maxScore <= 0:
            break

    print(maxPath)
    
    lastR = maxPath[-1][0]
    lastC = maxPath[-1][1]
    alignedA = a[lastC]
    alignedB = b[lastR]

    for (r,c) in list(reversed(maxPath[0:-1])):
        if not r == lastR:
            alignedB += b[r]
        else:
            alignedB += '-'
        if not c == lastC:
            alignedA += a[c]
        else:
            alignedA += '-'

        lastR = r
        lastC = c
    
    if debug:
        print("A: " + alignedA)
        print("B: " + alignedB)

    return alignmentScore
