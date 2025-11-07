import secrets
import math
from typing import Tuple


def is_probable_prime(n: int, k: int = 8) -> bool:

	if n < 2:
		return False
	small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
	for p in small_primes:
		if n % p == 0:
			return n == p

	s = 0
	d = n - 1
	while d % 2 == 0:
		d //= 2
		s += 1

	def try_composite(a: int) -> bool:
		x = pow(a, d, n)
		if x == 1 or x == n - 1:
			return False
		for _ in range(s - 1):
			x = (x * x) % n
			if x == n - 1:
				return False
		return True

	for _ in range(k):
		a = secrets.randbelow(n - 3) + 2
		if try_composite(a):
			return False
	return True


def generate_prime(bits: int) -> int:

	while True:
		p = secrets.randbits(bits) | (1 << (bits - 1)) | 1
		if is_probable_prime(p):
			return p


def egcd(a: int, b: int) -> Tuple[int, int, int]:
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = egcd(b % a, a)
		return (g, x - (b // a) * y, y)


def modinv(a: int, m: int) -> int:
	g, x, _ = egcd(a, m)
	if g != 1:
		raise ValueError("modular inverse does not exist")
	return x % m


def generate_keys(bits: int = 1024) -> Tuple[Tuple[int, int], Tuple[int, int]]:

	p = generate_prime(bits // 2)
	q = generate_prime(bits // 2)
	while q == p:
		q = generate_prime(bits // 2)

	n = p * q
	phi = (p - 1) * (q - 1)

	e = 65537
	if math.gcd(e, phi) != 1:
		while True:
			e = secrets.randbelow(phi - 2) + 2
			if math.gcd(e, phi) == 1:
				break

	d = modinv(e, phi)

	return (n, e), (n, d)


def encrypt(message: str, public_key: Tuple[int, int]) -> int:
	n, e = public_key
	m = int.from_bytes(message.encode("utf-8"), "big")
	if m >= n:
		raise ValueError("message too long for the key size; use a larger key or split the message")
	c = pow(m, e, n)
	return c


def decrypt(ciphertext: int, private_key: Tuple[int, int]) -> str:
	n, d = private_key
	m = pow(ciphertext, d, n)

	length = (m.bit_length() + 7) // 8
	if length == 0:
		return ""
	plaintext = m.to_bytes(length, "big").decode("utf-8", errors="ignore")
	return plaintext


def _demo():
	print("Generating RSA keys (512 bits for demo)...")
	public_key, private_key = generate_keys(bits=512)
	n_pub, e = public_key
	n_priv, d = private_key
	print("\nPublic key (n, e):")
	print(f"n = {n_pub}\ne = {e}")
	print("\nPrivate key (n, d):")
	print(f"n = {n_priv}\nd = {d}")

	msg = input('\nEnter a message to encrypt (or press Enter to use "Hello RSA"): ')
	if not msg:
		msg = "Hello RSA"

	ciphertext = encrypt(msg, public_key)
	print("\nCiphertext (hex):")
	print(hex(ciphertext))

	decrypted = decrypt(ciphertext, private_key)
	print("\nDecrypted plaintext:")
	print(decrypted)


if __name__ == "__main__":
	_demo()

