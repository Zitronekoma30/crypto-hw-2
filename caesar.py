import nltk
nltk.download('words')
from nltk.corpus import words
from collections import defaultdict

def caesar_cipher(text, z):
    result = ""
    text = text.lower()
    for i in range(len(text)):
        char = text[i]
        if char.isalpha():
            result += chr((ord(char) + z - 97) % 26 + 97)
        else:
            result += char
    return result

def caesar_decipher(text, z):
    return caesar_cipher(text, -z)

def brute_force_caesar(text):
    english_words = set(words.words())
    potential_matches = []

    for i in range(26):
        decrypted_text = caesar_decipher(text, i)
        decrypted_words = decrypted_text.split()

        if any(word in english_words for word in decrypted_words):
            potential_matches.append((i, decrypted_text))

    return potential_matches

def known_plaintext_attack(ciphertext, plaintext):
    shifts = defaultdict(int)
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha() and plaintext[i].isalpha():
            shift = ord(ciphertext[i]) - ord(plaintext[i])
            shifts[shift] += 1
    
    most_common_shift = max(shifts, key=shifts.get)
    if most_common_shift < 0:
        most_common_shift += 26
    return most_common_shift

plain =  "Conduct a known plaintext attack against the cipher implemented in task 9.) automatically find the z value used in the generated data."
msg1 = caesar_cipher(plain, 19)
print(msg1)

print(known_plaintext_attack(msg1, plain))
