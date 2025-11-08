#!/usr/bin/env python3
"""
hmac_demo.py
Generate HMACs with random key, verify them, and show negative tests.
"""
import hmac
import hashlib
import secrets
import binascii

def make_hmac(key, msg, algo):
    return hmac.new(key, msg, getattr(hashlib, algo)).hexdigest()

def main():
    key = secrets.token_bytes(16)  # 128-bit random key
    message = b"Transfer 1000 to Alice"

    print("HMAC demonstration")
    print("Secret key (hex):", binascii.hexlify(key).decode())
    print("Message:", message.decode())
    print()
    algos = ["sha1", "sha256", "sha512"]
    macs = {}
    for a in algos:
        mac = make_hmac(key, message, a)
        macs[a] = mac
        print(f"{a} HMAC: {mac}")

    print("\nVerify correct HMAC (sha512):")
    expected = macs["sha512"]
    calc = make_hmac(key, message, "sha512")
    print("  match:", hmac.compare_digest(calc, expected))

    print("\nNegative tests:")
    wrong_msg = b"Transfer 900 to Alice"
    wrong_key = secrets.token_bytes(16)
    print("  Wrong message valid?:", hmac.compare_digest(make_hmac(key, wrong_msg, "sha512"), expected))
    print("  Wrong key valid?:", hmac.compare_digest(make_hmac(wrong_key, message, "sha512"), expected))

if __name__ == "__main__":
    main()
