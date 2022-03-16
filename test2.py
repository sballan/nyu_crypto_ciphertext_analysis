import Levenshtein

def load_dictionary():
    with open("dictionary_2.txt") as f:
        # We first seek to location in the file where the words begin
        f.seek(10)
        # We read the words into an array
        return f.read().strip().split('\n')

def unigram_distribution(str):
    unigrams = {}

    for c in str:
        if c in unigrams:
            unigrams[c] += 1
        else:
            unigrams[c] = 1
    
    return unigrams

def digram_distribution(str):
    digrams = {}

    digram_list = [str[i:i+2] for i in range(0, len(str))]

    for digram in digram_list:
        if len(digram) < 2: break

        if digram in digrams:
            digrams[digram] += 1
        else:
            digrams[digram] = 1
    
    return digrams

def match_closest_word(str): 
    d_words = load_dictionary()
    
    closest_word = None
    closest_distance = 100000  # longer than any message we'll get
    
    for word in d_words:
        distance = Levenshtein.distance(str, word)
        if distance < closest_distance:
            closest_word = word
            closest_distance = distance

    return (closest_word, closest_distance)

def clean_text(text):
    valid_bigrams = set()
    d_words = load_dictionary()

    for word in d_words:
        valid_bigrams.add(" " + word[0])
        valid_bigrams.add(word[-1] + " ")

        for i in range(0, len(word) - 1):
            valid_bigrams.add(word[i:i+2])
        
    # With a list of all valid bigrams, we can clean up our text
    # If we have two invalid bigrams in a row of three characters, 
    # we can remove the middle character
    output = ""
    cursor = 0
    lookahead = cursor + 1

    while cursor < len(text):
        bigram1 = text[cursor:cursor+2]

        if bigram1 in valid_bigrams:
            output += bigram1[0]
            cursor += 1
            lookahead = cursor + 1
            next
        else:
            bigram2 = text[lookahead:lookahead+2]
            while (lookahead < len(text)-1) and (bigram2 not in valid_bigrams):
                lookahead += 1
                bigram2 = text[lookahead:lookahead+2]

            output += bigram1[0]

            if bigram2 in valid_bigrams:
                output


def decrypt(ciphertext):
    # First, we establish the distribution of characters
    d_text = ' '.join(load_dictionary())
    # unigrams
    d_udist = list(unigram_distribution(d_text).items())
    # bigrams
    d_ddist = list(digram_distribution(d_text).items())

    # These arrays of types are sorted by their second term, which is the frequency of the n-gram
    # d_udist is the distribution of unigrams
    d_udist.sort(key=lambda x: x[1], reverse=True)
    d_ddist.sort(key=lambda x: x[1], reverse=True)

    # c_udist is the distribution of unigrams
    c_udist = list(unigram_distribution(ciphertext).items())
    c_udist.sort(key=lambda x: x[1], reverse=True)

    key_map = {}

    for i in range(len(d_udist)):
        d_gram = d_udist[i][0]
        c_gram = c_udist[i][0]
        key_map[c_gram] = d_gram
    
    message_with_salt = ""
    for c in ciphertext:
        if key_map.get(c):
            message_with_salt += key_map[c]

    message = []
    for word in message_with_salt.split(' '):
        message.append(match_closest_word(word)[0])

    print(' '.join(message))
    # print(d_ddist)

if __name__ == "__main__":
    keygen(0)

if __name__ == "__main__2":
    # import sys
    # arg = sys.argv[1]

    with open('test2_ciphertext.txt', 'r') as f:
        ciphertext = f.readline()
    
    decrypt(ciphertext)

    # print(load_dictionary())
    # print(unigram_distribution('lacrosses protectional blistered leaseback assurers'))
    # print(digram_distribution('lacrosses protectional blistered leaseback assurers'))
