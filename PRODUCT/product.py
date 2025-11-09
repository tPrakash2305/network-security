def vigenere_encrypt(plaintext, keyword):
    plaintext = plaintext.upper().replace(" ", "")
    keyword = keyword.upper()
    ciphertext = ""
    key_length = len(keyword)

    for i in range(len(plaintext)):
        p = ord(plaintext[i]) - ord('A')
        k = ord(keyword[i % key_length]) - ord('A')
        c = (p + k) % 26
        ciphertext += chr(c + ord('A'))

    return ciphertext


def rail_fence_encrypt(text, num_rails):
    if num_rails == 1:
        return text

    rails = ['' for _ in range(num_rails)]
    row = 0
    direction_down = False

    for char in text:
        rails[row] += char
        if row == 0 or row == num_rails - 1:
            direction_down = not direction_down
        row += 1 if direction_down else -1

    return ''.join(rails)


def product_cipher_vigenere_railfence():
    plaintext = input("Enter the plaintext: ").upper().replace(" ", "")
    keyword = input("Enter the Vigenère keyword: ").upper()
    num_rails = 3

    vigenere_output = vigenere_encrypt(plaintext, keyword)
    print("After Vigenère Cipher:", vigenere_output)

    final_cipher = rail_fence_encrypt(vigenere_output, num_rails)
    print("Final Ciphertext (Product Cipher):", final_cipher)


# Run the product cipher function
product_cipher_vigenere_railfence()