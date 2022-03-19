# This file has an example implementation that uses a simple Levinshtein distance.
# It's main purpose is for benchmarking: can other methods beat this one, and by
# how much can they beat it?

import Levenshtein

from dictionary import Dictionary
from histkey import HistKeyGen


def decrypt(ciphertext, d_num, plaintext_length=500):
    dictionary = Dictionary(d_num)

    ciphertext_chardist = HistKeyGen(ciphertext).char_distribution()

    best_message = None
    best_quality = len(ciphertext)
    best_deckey = {}
    
    # Each dictionary "word" is a complete message for dictionary 1
    for message in dictionary.words():
        histkey = HistKeyGen(message, 0).__next__()
        deckey = {}

        for i in range(len(histkey)):
            d_char = histkey[i]
            c_char = ciphertext_chardist[i][0]
            deckey[c_char] = d_char

        m_rchars = ""
        for c in ciphertext:
            if deckey.get(c):
                m_rchars += deckey[c]
            else:
                raise BaseException("deckey is missing a character!")

        distance = Levenshtein.distance(m_rchars, ciphertext)
        quality = distance / len(ciphertext)

        if quality < best_quality:
            best_message = message
            best_quality = quality
            best_deckey = deckey

    return best_message, best_quality, best_deckey
    
        