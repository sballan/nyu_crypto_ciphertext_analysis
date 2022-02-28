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
    unigrams = {}

    for c in ciphertext:
        if c in unigrams:
            unigrams[c] += 1
        else:
            unigrams[c] = 1



if __name__ == "__main__":
    import sys
    # arg = sys.argv[1]

    # print(load_dictionary())
    print(unigram_distribution('lacrosses protectional blistered leaseback assurers'))
    print(digram_distribution('lacrosses protectional blistered leaseback assurers'))