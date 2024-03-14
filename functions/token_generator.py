import random
import string


def generate(length):
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    return rand_string

def tokenize():
    token = generate(24)
    return token
