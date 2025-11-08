#!/usr/bin/env python3
"""
hash_demo.py
Compute and display hashes for sample messages with common algorithms.
"""
import hashlib

msgs = [b"", b"hello", b"hello!", b"Hello", b"hello world"]
algs = ["md5", "sha1", "sha256", "sha512"]

def hexdigest(algo, data):
    h = hashlib.new(algo)
    h.update(data)
    return h.hexdigest()

def main():
    print("Hash demonstration\n")
    for a in algs:
        print(f"Algorithm: {a} (digest size: {hashlib.new(a).digest_size*8} bits)")
        for m in msgs:
            txt = m.decode("utf-8", "replace")
            print(f"  '{txt}': {hexdigest(a, m)}")
        print()

if __name__ == "__main__":
    main()
