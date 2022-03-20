# This file has an example implementation that uses a simple Levinshtein distance.
# It's main purpose is for benchmarking: can other methods beat this one, and by
# how much can they beat it?
import ray
import Levenshtein

from .dictionary import Dictionary
from .histkey import HistKeyGen


def decryption_with_histkey(message, ciphertext, histkey):
    ciphertext_chardist = HistKeyGen(ciphertext).char_distribution()
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

    distance = Levenshtein.distance(m_rchars, message)
    quality = distance / len(ciphertext)
    return message, quality


@ray.remote
def perform_decryption_with_histkey(message, ciphertext, histkey):
    return decryption_with_histkey(message, ciphertext, histkey)


def decrypt(ciphertext, d_num):
    dictionary = Dictionary(d_num)

    CHUNK_SIZE = 1000
    KEY_LIMIT = 1000

    best_message = None
    best_quality = 1
    best_deckey = {}
    
    # Each dictionary "word" is a complete message for dictionary 1
    for message in dictionary.words():
        hk_generator = HistKeyGen(message, 0)

        task_refs = []
        for histkey in hk_generator:
            ref = perform_decryption_with_histkey.remote(message, ciphertext, histkey)
            task_refs.append(ref)
            counter += 1

            if (counter % CHUNK_SIZE) == 0 or (counter > KEY_LIMIT):
                results = ray.get(task_refs)
                task_refs = []

                for message, quality, deckey in results:
                    if quality < best_quality:
                        best_quality = quality
                        best_message = message
                        best_deckey = deckey

                print(f"Processed chunk at {counter}!")

            if counter > KEY_LIMIT:
                print("Finished the chunks!")
                break

        # If the keyspace is small, we'll have leftovers
        leftovers = ray.get(task_refs)
        if len(leftovers) > 0:
            for message, quality, deckey in leftovers:
                if quality < best_quality:
                    best_quality = quality
                    best_message = message
                    best_deckey = deckey

        return best_message, best_quality, best_deckey
        
            