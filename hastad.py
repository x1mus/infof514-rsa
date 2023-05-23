from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes
import math, gmpy2

secret = b"Cryptanalysis course is awesome!"

key0 = RSA.generate(1024, e=3)
key1 = RSA.generate(1024, e=3)
key2 = RSA.generate(1024, e=3)
c0 = pow(bytes_to_long(secret), 3, key0.n)
c1 = pow(bytes_to_long(secret), 3, key1.n)
c2 = pow(bytes_to_long(secret), 3, key2.n)

N = [key0.n, key1.n, key2.n]
c = [c0, c1, c2]

def crt(N, c):
	final = c[0]

	for i in range(1,len(N)):
		new_N = math.prod(N[:i])
		remainder = (c[i] - final) % N[i]
		inverse = pow(new_N, -1, N[i])
		local_solution = remainder*inverse % N[i]
		final = local_solution * new_N + final

	return final

print(long_to_bytes(gmpy2.iroot(crt(N, c), 3)[0]))