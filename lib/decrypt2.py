import Levenshtein
import ray
from statistics import mean

from histkey import HistKeyGen
from dictionary import Dictionary


def dictionary_string():
    with open("dictionary_2.txt") as f:
        # We first seek to location in the file where the words begin
        f.seek(10)
        # We return a newline separated list of dictionary words, with leading
        #  and trailing whitespace removed
        return f.read().strip().replace("\n", " ")


def dictionary_words():
    return dictionary_string().split(" ")


def match_closest_word(str, d_words):
    closest_word = None
    closest_distance = 100000  # longer than any message we'll get

    for word in d_words:
        distance = Levenshtein.distance(str, word)
        if distance < closest_distance:
            closest_word = word
            closest_distance = distance

    return (closest_word, closest_distance)


def decryption_with_histkey(ciphertext, histkey, d_num, plaintext_length=500):
    dictionary = Dictionary(d_num)
    # We can use the HistKeyGen class to generate a character distribution for us.
    # We don't need any of it's other functions
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

    ps = 0  # start pointer
    pe = 0  # end pointer
    pl = pe  # lookahead pointer

    message = []
    match_qualities = []
    while pe < len(m_rchars):
        # skip ahead to the next space
        while pe < len(m_rchars) - 1 and m_rchars[pe] != " ":
            pe += 1

        if m_rchars[pe] == " ":
            substr = m_rchars[ps:pe]
            f_word, f_dist = match_closest_word(substr, dictionary.words())

            match_quality = f_dist / len(substr)

            lookahead_checked = False
            while lookahead_checked == False:
                pl = pe + 1
                l_match_quality = -1  # -1 means no match has been found
                # skip ahead to the next space
                while pl < len(m_rchars) - 1 and m_rchars[pl] != " ":
                    pl += 1

                if m_rchars[pl] == " ":
                    l_substr = m_rchars[ps:pl]
                    lf_word, lf_dist = match_closest_word(l_substr, dictionary.words())

                    l_match_quality = lf_dist / len(l_substr)
                    if l_match_quality < 0:
                        raise ("l_match_quality cannot be less than zero!")

                    if l_match_quality < match_quality:
                        substr = l_substr
                        f_word, f_dist = lf_word, lf_dist
                        match_quality = l_match_quality
                        pe = pl
                    else:
                        lookahead_checked = True
                else:
                    lookahead_checked = True

            match_qualities.append(match_quality)
            message.append(f_word)
            ps = pe + 1
            pe += 2
        else:
            leftover = plaintext_length - len(" ".join(message))
            partial_dict_words = [word[0 : leftover - 1] for word in dictionary.words()]
            substring = m_rchars[ps:pe]

            f_word, f_dist = match_closest_word(substring, partial_dict_words)
            match_qualities.append(f_dist / max(len(substring), len(f_word)))
            message.append(f_word)

            pe += 1

    return " ".join(message), mean(match_qualities), deckey


@ray.remote
def perform_decryption_with_histkey(ciphertext, histkey, d_num,  plaintext_length=500):
    return decryption_with_histkey(ciphertext, histkey, d_num, plaintext_length)


def decrypt(ciphertext, d_num, plaintext_length=500):
    ray.init()

    dictionary = Dictionary(d_num)
    hk_generator = HistKeyGen(dictionary.string(), 1)

    CHUNK_SIZE = 1000
    KEY_LIMIT = 10000
    counter = 0
    task_refs = []

    best_message = ""
    best_quality = 99999999
    best_deckey = None

    for histkey in hk_generator:
        ref = perform_decryption_with_histkey.remote(ciphertext, histkey, d_num, plaintext_length)
        task_refs.append(ref)
        counter += 1

        if (counter % CHUNK_SIZE) == 0:
            tasks_chunk = task_refs[:CHUNK_SIZE]
            task_refs = task_refs[CHUNK_SIZE:]

            results = ray.get(tasks_chunk)

            for message, quality, deckey in results:
                if quality < best_quality:
                    best_quality = quality
                    best_message = message
                    best_deckey = deckey

            print(f"Processed chunk at {counter}!")

        if counter > KEY_LIMIT:
            print("Finished the chunks!")
            break

    print("Let's return the chunks")

    ray.shutdown()
    return best_message, best_quality, best_deckey


if __name__ == "__main__":
    # import sys
    # arg = sys.argv[1]

    with open("test2_plaintext.txt", "r") as f:
        plaintext = f.readline().strip()

    with open("test2_ciphertext.txt", "r") as f:
        ciphertext = f.readline().strip()
        # ciphertext = f.readline().strip()

    message, quality, deckey = decrypt(ciphertext, 2)

    print(
        f"Our guess quality was {quality}, where the expected quality is {(len(ciphertext) - len(plaintext)) / len(ciphertext)}"
    )
    print(f"Our guess was {Levenshtein.distance(message, plaintext)} away")
    print(f"Our key was: {deckey}")
    print(f"Guess: \n{message}")

    # print(dictionary_words())
    # print(unigram_distribution('lacrosses protectional blistered leaseback assurers'))
    # print(digram_distribution('lacrosses protectional blistered leaseback assurers'))
