import Levenshtein
import ray
from statistics import mean

from histkey import HistKeyGen
from dictionary import Dictionary


def match_closest_word(str, d_words):
    closest_word = ""
    closest_distance = len(str)  # longer than any message we'll get

    for word in d_words:
        # The word length cannot be greater than the ciphertext substring length
        if len(word) > len(str):
            continue

        distance = Levenshtein.distance(str, word)
        if (distance < closest_distance) or (
            (distance == closest_distance) and len(word) > len(closest_word)
        ):
            closest_word = word
            closest_distance = distance

    return (closest_word, closest_distance)


def decryption_with_histkey(ciphertext, histkey, d_words, plaintext_length=500):
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
        else:
            raise BaseException("deckey is missing a character!")

    ps = 0  # start pointer
    pe = 1  # end pointer
    pl = pe  # lookahead pointer

    message = []
    match_qualities = []
    while pe < len(m_rchars):
        # skip ahead to the next space
        while pe < len(m_rchars) - 1 and m_rchars[pe] != " ":
            pe += 1

        if m_rchars[pe] == " ":
            substr = m_rchars[ps:pe]
            f_word, f_dist = match_closest_word(substr, d_words)

            match_quality = f_dist / len(substr)

            lookahead_checked = False
            while lookahead_checked == False:
                pl = pe + 1
                l_match_quality = -1  # -1 means no match has been found
                # skip ahead to the next space
                while pl < len(m_rchars) - 1 and m_rchars[pl] != " ":
                    pl += 1

                if pl < len(m_rchars) and m_rchars[pl] == " ":
                    l_substr = m_rchars[ps:pl]
                    lf_word, lf_dist = match_closest_word(l_substr, d_words)

                    l_match_quality = lf_dist / len(l_substr)
                    if l_match_quality < 0:
                        raise BaseException("l_match_quality cannot be less than zero!")

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
            # pe is a space, we now want to start one after that space
            ps = pe + 1
            pe += 2
        else:
            leftover = plaintext_length - len(" ".join(message))
            partial_dict_words = [word[0 : leftover - 1] for word in d_words]
            substring = m_rchars[ps:pe]

            f_word, f_dist = match_closest_word(substring, partial_dict_words)
            match_qualities.append(f_dist / len(substring))
            message.append(f_word)

            pe += 1

    return " ".join(message), mean(match_qualities), deckey


@ray.remote
def perform_decryption_with_histkey(ciphertext, histkey, d_words, plaintext_length=500):
    return decryption_with_histkey(ciphertext, histkey, d_words, plaintext_length)


def decrypt(ciphertext, d_num, plaintext_length=500):
    ray.init(num_cpus=4)

    dictionary = Dictionary(d_num)
    d_words = dictionary.words()
    hk_generator = HistKeyGen(dictionary.string(), 1)

    CHUNK_SIZE = 10000
    KEY_LIMIT = 100000
    counter = 0
    task_refs = []

    best_message = ""
    best_quality = 99999999
    best_deckey = None

    for histkey in hk_generator:
        ref = perform_decryption_with_histkey.remote(
            ciphertext, histkey, d_words, plaintext_length
        )
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

            #print(f"Processed chunk at {counter}!")

        if counter > KEY_LIMIT:
            #print("Finished the chunks!")
            break

    # If the keyspace is small, we'll have leftovers
    leftovers = ray.get(task_refs)
    if len(leftovers) > 0:
        for message, quality, deckey in leftovers:
            if quality < best_quality:
                best_quality = quality
                best_message = message
                best_deckey = deckey

        #print(f"Processed chunk at {counter + 1}!")

    #print("Let's return the chunks")

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

