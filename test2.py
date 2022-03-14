import Levenshtein
from functools import cache

@cache
def dictionary_string():
    with open("dictionary_2.txt") as f:
        # We first seek to location in the file where the words begin
        f.seek(10)
        # We return a newline separated list of dictionary words, with leading
        #  and trailing whitespace removed
        return f.read().strip().replace("\n", " ")

@cache
def dictionary_words():
    return dictionary_string().split(' ')

def unigram_distribution(str):
    unigrams = {}

    for c in str:
        if c in unigrams:
            unigrams[c] += 1
        else:
            unigrams[c] = 1
    
    return unigrams

def match_closest_word(str, d_words): 
    closest_word = None
    closest_distance = 100000  # longer than any message we'll get
    
    for word in d_words:
        distance = Levenshtein.distance(str, word)
        if distance < closest_distance:
            closest_word = word
            closest_distance = distance

    return (closest_word, closest_distance)

def decrypt(ciphertext, plaintext_length=500):
    # First, we establish the distribution of characters
    d_text = dictionary_string()
    # unigrams
    d_udist = list(unigram_distribution(d_text).items())
    # bigrams
    # d_ddist = list(digram_distribution(d_text).items())

    # These arrays of types are sorted by their second term, which is the frequency of the n-gram
    # d_udist is the distribution of unigrams
    d_udist.sort(key=lambda x: x[1], reverse=True)
    # d_ddist.sort(key=lambda x: x[1], reverse=True)

    # c_udist is the distribution of unigrams
    c_udist = list(unigram_distribution(ciphertext).items())
    c_udist.sort(key=lambda x: x[1], reverse=True)

    key_map = {}

    for i in range(len(d_udist)):
        d_gram = d_udist[i][0]
        c_gram = c_udist[i][0]
        key_map[c_gram] = d_gram
    
    m_rchars = ""
    for c in ciphertext:
        if key_map.get(c):
            m_rchars += key_map[c]

    ps = 0 # start pointer
    pe = 0 # end pointer
    pl = pe # lookahead pointer

    message = []
    while pe < len(m_rchars):
        # skip ahead to the next space
        while pe < len(m_rchars)-1 and m_rchars[pe] != ' ': 
            pe += 1

        if m_rchars[pe] == " ":
            substr = m_rchars[ps:pe]
            f_word, f_dist = match_closest_word(substr, dictionary_words())

            match_quality = f_dist / len(substr)

            lookahead_checked = False
            while lookahead_checked == False: 
                pl = pe + 1
                l_match_quality = -1 # -1 means no match has been found
                # skip ahead to the next space
                while pl < len(m_rchars)-1 and m_rchars[pl] != ' ': 
                    pl += 1

                if m_rchars[pl] == ' ':
                    l_substr = m_rchars[ps:pl]
                    lf_word, lf_dist = match_closest_word(l_substr, dictionary_words())

                    l_match_quality = lf_dist / len(l_substr)
                    if l_match_quality < 0: raise("l_match_quality cannot be less than zero!")

                    if l_match_quality < match_quality:
                        substr = l_substr
                        f_word, f_dist = lf_word, lf_dist
                        match_quality = l_match_quality
                        pe = pl
                    else: 
                        lookahead_checked = True
                else: 
                    lookahead_checked = True
           
            message.append(f_word)
            ps = pe + 1
            pe += 2
        else:
            leftover = (plaintext_length - len(' '.join(message)))
            partial_dict_words = [word[0:leftover+1] for word in dictionary_words()]
            
            f_word, f_dist = match_closest_word(m_rchars[ps:pe], partial_dict_words)
            message.append(f_word)

            pe += 1
            
    return ' '.join(message)




if __name__ == "__main__":
    # import sys
    # arg = sys.argv[1]

    with open('test2_plaintext.txt', 'r') as f:
        plaintext = f.readline().strip()

    with open('test2_ciphertext.txt', 'r') as f:
        ciphertext = f.readline().strip()
    
    attempt = decrypt(ciphertext)

    print(f"Our guess was {Levenshtein.distance(attempt, plaintext)} away")
    print(f"Guess: \n{attempt}")

    # print(dictionary_words())
    # print(unigram_distribution('lacrosses protectional blistered leaseback assurers'))
    # print(digram_distribution('lacrosses protectional blistered leaseback assurers'))
