# based on https://crypto.stackexchange.com/questions/6361/is-sharing-the-modulus-for-multiple-rsa-key-pairs-secure/14713
# https://fr.wikipedia.org/wiki/Test_de_primalit%C3%A9_de_Miller-Rabin
from Crypto.PublicKey import RSA
import math
import random


def getModInverse(a, m):
    if math.gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m

    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (
            u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


key = RSA.generate(2048)
phi = (key.p-1)*(key.q-1)
d_2 = getModInverse(76637, phi)
key_2 = RSA.construct((key.n, 76637, d_2, key.p, key.q))

N = key.n
p = key.p
q = key.q

k = (key.e * key.d) - 1


def get_r_t(k):
    r = k
    t = 0
    while (r & 1) == 0:
        t = t + 1
        r = r >> 1
    return r, t


def factorise_N(N, e, d):
    r, t = get_r_t((e * d) - 1)
    solution = False
    while not solution:
        x = random.randrange(2, N)
        if math.gcd(x, N) != 1:
            continue
        result = pow(x, r, N)
        old_result = result
        if result == 1:
            continue
        while result != 1 and old_result != 1:
            old_result = result
            result = pow(result, 2, N)
        if old_result == -1 or old_result == N-1:
            continue
        else:
            p_1 = math.gcd(old_result-1, N)
            q_1 = N // p_1
            if (p_1 != p or q_1 != q) and (p_1 != q or q_1 != p):
                print('error')
            solution = True
            print('success')
            print(p, q)
