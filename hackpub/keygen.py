import random

LETTERS = "abcdefghijklmnopqrstuvwxyz"

def generate_random_word(length):
    letters = []
    for i in range(length):
        letters.append(random.choice(LETTERS))
    return ''.join(letters)
