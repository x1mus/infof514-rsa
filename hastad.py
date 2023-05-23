import math, gmpy2

N = [7, 5, 12]
c = [3, 3, 4]

def crt(N, c):
	final = c[0]

	for i in range(1,len(N)):
		new_N = math.prod(N[:i])
		remainder = (c[i] - final) % N[i]
		inverse = pow(new_N, -1, N[i])
		local_solution = remainder*inverse % N[i]
		final = local_solution * new_N + final

	return final

print(gmpy2.iroot(crt(N, c), 3)[0])