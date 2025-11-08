#!/usr/bin/env python3
"""
avalanche.py
Demonstrate avalanche effect: flip a single bit and measure bit differences in hashes.
"""
import hashlib
import binascii

def bit_diff(b1, b2):
    return sum(bin(x ^ y).count("1") for x, y in zip(b1, b2))

def hash_diff(algo, m1, m2):
    h1 = hashlib.new(algo, m1).digest()
    h2 = hashlib.new(algo, m2).digest()
    diffs = bit_diff(h1, h2)
    return len(h1) * 8, diffs

def main():
    m = bytearray(b"this is a test message for avalanche")
    m2 = bytearray(m)
    # flip single bit in last byte
    m2[-1] ^= 1

    algos = ["sha1", "sha256", "sha512"]
    print("Avalanche effect test\n")
    print("Original message:", m.decode())
    print("Modified message:", m2.decode())
    print()
    for a in algos:
        total_bits, diffs = hash_diff(a, m, m2)
        pct = diffs / total_bits * 100.0
        print(f"{a}: {diffs}/{total_bits} bits different ({pct:.2f}%)")

if __name__ == "__main__":
    main()
