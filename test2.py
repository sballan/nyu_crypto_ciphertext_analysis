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

def decrypt(ciphertext):
    # First, we establish the distribution of characters
    d_text = ' '.join(load_dictionary())
    d_udist = list(unigram_distribution(d_text).items())
    d_ddist = list(digram_distribution(d_text).items())

    # These arrays of types are sorted by their second term, which is the frequency of the n-gram
    d_udist.sort(key=lambda x: x[1], reverse=True)
    d_ddist.sort(key=lambda x: x[1], reverse=True)

    print(d_udist)
    # print(d_ddist)




if __name__ == "__main__":
    # import sys
    # arg = sys.argv[1]

    with open('test2_ciphertext.txt', 'r') as f:
        ciphertext = f.readline()
    
    decrypt(ciphertext)

    # print(load_dictionary())
    # print(unigram_distribution('lacrosses protectional blistered leaseback assurers'))
    # print(digram_distribution('lacrosses protectional blistered leaseback assurers'))