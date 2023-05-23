
from math import gcd


def pollardp1(base, bound, N):
    a = base
    for j in range(2, bound):
        a = pow(a,j,N)
        d = gcd(a-1, N)
        if d != 1:
            return d, N//d

print(pollardp1(2, 100, 13927189))