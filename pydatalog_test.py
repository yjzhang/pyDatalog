from pyDatalog.pyDatalog import create_terms

create_terms('X,Y,Z,N0,N1,N2')
create_terms('abc,answer')

+abc('a','b','c')
abc(X,Y,Z) <= abc(X[0],Y[0],Z[0]) & abc(X[1:],Y[1:],Z[1:])

print(abc('aa','bb','cc'))

create_terms('len0, len1')

answer(X,N1,N2) <= (abc(X[0:N1],X[N1:N2],X[N2:]))

(X=='aabbcc') & (N0.in_(range(len(X.data[0])))) & (N1.in_(range(len(X.data[0])))) & answer(X,N0,N1)

create_terms('rep1,N')


rep1(X,Y,N) <= rep1(X[N:], X[:N], N0)

#len0(X, N0) <= (0 <= N0) & (N0 < len(X))

#len0('', X) <= 0

