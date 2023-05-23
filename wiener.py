from fractions import Fraction

import random, math, gmpy2, cmath
from Crypto.Util import number

import owiener

def keygen():
	p, q = 0, 0
	while not(p < q and q < 2*p): # p < q < 2p
		p = number.getPrime(512)
		q = number.getPrime(512)

	n = p*q
	phi = (p-1)*(q-1)

	max_d = int(pow(n,(1/4)) // 3) # d < (n**(1/4))/3
	while True:
		d = random.getrandbits(max_d.bit_length()-1)
		if math.gcd(d, phi) == 1:
			e = pow(d, -1, phi)
			break

	print(f"p = {str(p)[:50]}...")
	print(f"q = {str(q)[:50]}...")
	print(f"n = {str(n)[:50]}...")
	print(f"φ = {str(phi)[:50]}...")
	print(f"e = {str(e)[:50]}...")
	print(f"d = {str(d)[:50]}...")

	return (n,e)

def quadratic(n, phi):
	a = 1
	b = -(n - phi + 1)
	c = n

	delta = b**2 - (4*a*c)
	square = gmpy2.sqrt(delta)
	isquare = gmpy2.isqrt(delta)
	if square == isquare:
		p = (-b+isquare)//(2*a)
		q = (-b-isquare)//(2*a)
		return (p,q)
	else:
		return (0.1, 0.1)

def compute_fraction(q_list):
	q_list = list(reversed(q_list))
	
	num, den = 1, q_list[0]
	for i in range(len(q_list)-2):
		saved_den = den
		den = den*q_list[i+1] + num
		num = saved_den

	if q_list[-1] != 0:
		num = den*q_list[-1] + num
	
	#print(f"{num}/{den}")

	return (num, den)

def check_validity(n, e, k, d):
	# Check if d is odd and k != 0:
	if d % 2 == 1 and k != 0:
		phi = gmpy2.div((e*d)-1, k)
		# Verify that phi is a whole number
		if phi == int(phi):
			p, q = quadratic(n, phi)
			if p == int(p) and q == int(q): # Verify that the roots are whole numbers
				print(f"Result: d={d},k={k},p={int(p)},q={int(q)}")
				return True
			else:
				return False
		else:
			return False
	else:
		return False

def wiener(n, e):
	x = e
	y = n
	r = None
	q_list = []
	while r != 0:
		# Initial computation
		r = x % y
		q = x // y
		q_list.append(q)

		# Compute fractions
		k, d = compute_fraction(q_list)
		print(f"{k}/{d}")

		# Check for parameters validity
		#if check_validity(n, e, k, d):
		#	break

		# Update for next step
		x = y
		y = r
	print(q_list)

if __name__ == "__main__":
	print("Private vulnerable key generation")
	n, e = keygen()

	print()
	print("Wiener's attack")
	wiener(n, e)

	print()
	print("OWiener implementation")
	print(f"d = {owiener.attack(e, n)}")

	print()
	print("Example with N=64741 and e=42667")
	wiener(64741, 42667)