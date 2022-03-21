# This file has an example implementation that uses a simple Levinshtein distance.
# It's main purpose is for benchmarking: can other methods beat this one, and by
# how much can they beat it?
import ray
import Levenshtein
import statistics
import encryption

from dictionary import Dictionary
from histkey import HistKeyGen


def decryption_with_histkey(message, ciphertext, histkey):
    ciphertext_chardist = HistKeyGen(ciphertext).char_distribution()
    deckey = {}

    for i in range(len(histkey)):
        d_char = histkey[i]
        c_char = ciphertext_chardist[i][0]
        deckey[c_char] = d_char

    m_rchars = []
    for c in ciphertext:
        if deckey.get(c):
            m_rchars.append(deckey[c])
        else:
            raise BaseException("deckey is missing a character!")
    m_rchars = "".join(m_rchars)

    distance = Levenshtein.distance(m_rchars, message)
    quality = distance / len(ciphertext)
    return message, quality, deckey


@ray.remote
def perform_decryption_with_histkey(message, ciphertext, histkey):
    return decryption_with_histkey(message, ciphertext, histkey)


def decrypt(ciphertext, d_num):
    ray.init(num_cpus=4)

    dictionary = Dictionary(d_num)

    CHUNK_SIZE = 1000
    KEY_LIMIT = 10000

    best_message = None
    best_quality = 1
    best_deckey = {}
    message_results = []
    # Each dictionary "word" is a complete message for dictionary 1
    for message in dictionary.words():
        local_best_quiality = 1
        hk_generator = HistKeyGen(message, 0, 2)
        counter = 0

        task_refs = []

        for histkey in hk_generator:
            ref = perform_decryption_with_histkey.remote(message, ciphertext, histkey)
            task_refs.append(ref)
            counter += 1

            if (counter % CHUNK_SIZE) == 0 or (counter > KEY_LIMIT):
                results = ray.get(task_refs)
                task_refs = []

                for message, quality, deckey in results:
                    if quality < local_best_quiality:
                        local_best_quiality = quality
                    if quality < best_quality:
                        best_quality = quality
                        best_message = message
                        best_deckey = deckey

                # print(f"Processed chunk at {counter}!")

            if counter > KEY_LIMIT:
                # print("Finished the chunks!")
                break

        # If the keyspace is small, we'll have leftovers
        leftovers = ray.get(task_refs)
        if len(leftovers) > 0:
            for message, quality, deckey in leftovers:
                if quality < local_best_quiality:
                    local_best_quiality = quality

                if quality < best_quality:
                    best_quality = quality
                    best_message = message
                    best_deckey = deckey
        message_results.append([message, local_best_quiality])

    message_results.sort(key=lambda x: x[1], reverse=True)
    quality_values = []
    for i in message_results:
        quality_values.append(i[1])
    std = statistics.stdev(quality_values[:-1])
    zscore = (statistics.mean(quality_values[:-1]) - quality_values[-1]) / std

    ray.shutdown()
    return best_message, zscore

if __name__ == "__main__":
    encryption.test_decryption_algorithm(decrypt, 1)
