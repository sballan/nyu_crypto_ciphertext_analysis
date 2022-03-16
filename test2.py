from statistics import mean
import Levenshtein
import ray
from functools import cache
from itertools import permutations

ray.init()

class HistKeyGen:
    """
    "Histogram Key Generator".  The HistKey is an array of characters that can be used
    to generate a key given a particular ciphertext.  For a given ciphertext, there is
    a bijection between HistKeys and keys.
    """

    def __init__(self, d_text, tolerance=0):
        self.d_text = d_text
        self.tolerance = tolerance

        chunks = self.create_chunks()

        chunks.reverse() # This is a funny optimization

        # Each item in `chunk_perms` is an array containing all the permutations for the 
        # corresponding chunk in the `chunks` array
        self.chunk_perms = [list(permutations(chunk)) for chunk in chunks]

        # We keep track of which permutation we're considering for each chunk
        self.chunk_ptrs = [0 for _ in chunks]
        # A useful variable for the top of our "stack"
        self.stack_top = len(chunks)-1
        # We use a stack metaphor, since we recurse up and down the chunk_perms, resetting
        # the "top" of the stack as we go "down" the stack. This algorithm could have be implemented
        # using an actual stack, but I think this is simpler conceptually
        self.stack_ptr = self.stack_top
    

    def __next__(self):
        if self.stack_ptr >= 0:
            key = []
            while len(key) == 0:
                if self.stack_top == self.stack_ptr:
                    """
                    We're at the top of the stack, so there is the possibility that we may return a key. 
                    If the chunk pointer hasn't gotten to the end yet, we can take a snapshot of the whole
                    stack to create a new key and return it.  Otherwise, we need to pop the top chunk off 
                    the stack.  We do this by setting its chunk pointer to zero, and decrementing the stack pointer.
                    """
                    if self.chunk_ptrs[self.stack_top] < len(self.chunk_perms[self.stack_top]):
                        for i, ptr in enumerate(self.chunk_ptrs):
                            key.extend(self.chunk_perms[i][ptr])

                        self.chunk_ptrs[self.stack_top] += 1
                    else:
                        self.chunk_ptrs[self.stack_top] = 0
                        self.stack_ptr -= 1
                else:
                    """
                    We're not at the top of the stack. If we can, we'll increment the pointer we're looking
                    at, and then go back to the top of the stack (ie, "put everything back on the stack").
                    If we can't, we need pop this chunk off the stack. We do this by setting the chunk pointer
                    to zero, and decrementing the stack pointer.
                    """
                    if self.stack_ptr >= 0:
                        if self.chunk_ptrs[self.stack_ptr] < len(self.chunk_perms[self.stack_ptr])-1:
                            self.chunk_ptrs[self.stack_ptr] += 1
                            self.stack_ptr = self.stack_top
                        else:
                            self.chunk_ptrs[self.stack_ptr] = 0
                            self.stack_ptr -= 1 
                    else:
                        raise(StopIteration)  
                           
            key.reverse()
            return key
        else:
            raise(StopIteration)



    def __iter__(self):
        """Needed to conform to the iterator interface"""
        return self


    def create_chunks(self):
        char_dist = self.char_distribution()
        # This chunking procedure groups the characters into arrays where each sequence of characteres
        # has a similar frequency
        chunks = [[]]
        for i, c_t in enumerate(char_dist):
            if len(chunks[-1]) == 0:
                chunks[-1].append(c_t[0])
                continue

            last_freq = char_dist[i-1][1]
            if (last_freq - c_t[1]) <= self.tolerance:  # TODO: consider adding a condition here which limits size of chunk
                chunks[-1].append(c_t[0])
                continue
            else:
                chunks.append([c_t[0]])
                continue
        
        return chunks
    

    def char_distribution(self):
        """
        Character distribution of the dictionary text, as a sorted list of tuples (char, frequency)
        """
        chars = {}

        for c in self.d_text:
            if c in chars:
                chars[c] += 1
            else:
                chars[c] = 1

        # Get the distribution as a list, so we can sort it
        char_dist = list(chars.items())
        # We sort the list by the second item in each tuple, which is the frequency of the 
        # character. The result is a list of characters sort from most to least frequent
        char_dist.sort(key=lambda x: x[1], reverse=True)

        return char_dist


# @cache
def dictionary_string():
    with open("dictionary_2.txt") as f:
        # We first seek to location in the file where the words begin
        f.seek(10)
        # We return a newline separated list of dictionary words, with leading
        #  and trailing whitespace removed
        return f.read().strip().replace("\n", " ")

# @cache
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

def keygen(tolerance=1):
    # First, we establish the distribution of characters
    d_text = dictionary_string()
    # character distribution
    char_dist = list(unigram_distribution(d_text).items())
    # We sort the list by the second item in each tuple, which is the frequency of the 
    # character. The result is a list of characters sort from most to least frequent
    char_dist.sort(key=lambda x: x[1], reverse=True)

    # This chunking procedure groups the characters into arrays where each sequence of characteres
    # has a similar frequency
    chunks = [[]]
    for i, c_t in enumerate(char_dist):
        if len(chunks[-1]) == 0:
            chunks[-1].append(c_t[0])
            continue

        last_freq = char_dist[i-1][1]
        if (last_freq - c_t[1]) <= tolerance:  # TODO: consider adding a condition here which limits size of chunk
            chunks[-1].append(c_t[0])
            continue
        else:
            chunks.append([c_t[0]])
            continue

    # Each item in `chunk_perms` is an array containing all the permutations for the 
    # corresponding chunk in the `chunks` array
    chunk_perms = [list(permutations(chunk)) for chunk in chunks]

    # We keep track of which permutation we're considering for each chunk
    chunk_ptrs = [0 for _ in chunks]
    # A useful variable for the top of our "stack"
    stack_top = len(chunks)-1
    # We use a stack metaphor, since we recurse up and down the chunk_perms, resetting
    # the "top" of the stack as we go "down" the stack. This algorithm could have be implemented
    # using an actual stack, but I think this is simpler conceptually
    stack_ptr = stack_top

    keys = []

    while stack_ptr >= 0:
        if stack_top == stack_ptr:
            if chunk_ptrs[stack_top] < len(chunk_perms[stack_top]):
                key = []
                for i, ptr in enumerate(chunk_ptrs):
                    key.extend(chunk_perms[i][ptr])
                keys.append(key)        
                chunk_ptrs[stack_top] += 1
            else:
                chunk_ptrs[stack_top] = 0
                stack_ptr -= 1
        else:
            if chunk_ptrs[stack_ptr] < len(chunk_perms[stack_ptr])-1:
                chunk_ptrs[stack_ptr] += 1
                stack_ptr = stack_top
            elif stack_ptr >= 0: 
                chunk_ptrs[stack_ptr] = 0
                stack_ptr -= 1

    return keys

@ray.remote
def perform_decryption_with_histkey(ciphertext, histkey, plaintext_length=500):
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

    ps = 0 # start pointer
    pe = 0 # end pointer
    pl = pe # lookahead pointer

    message = []
    match_qualities = []
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

            match_qualities.append(match_quality)
            message.append(f_word)
            ps = pe + 1
            pe += 2
        else:
            leftover = (plaintext_length - len(' '.join(message)))
            partial_dict_words = [word[0:leftover+1] for word in dictionary_words()]
            substring = m_rchars[ps:pe]

            f_word, f_dist = match_closest_word(substring, partial_dict_words)
            match_qualities.append(f_dist / max(len(substring), len(f_word)))
            message.append(f_word)

            pe += 1
            
    return ' '.join(message), mean(match_qualities)


def decrypt(ciphertext, plaintext_length=500):
    hk_generator = HistKeyGen(dictionary_string(), 1)

   
    CHUNK_SIZE = 2000
    KEY_LIMIT = 20000
    counter = 0
    task_refs = []

    best_message = ""
    best_quality = 99999999

    for histkey in hk_generator:
        ref = perform_decryption_with_histkey.remote(ciphertext, histkey)
        task_refs.append(ref)
        counter += 1

        if counter > CHUNK_SIZE:
            tasks_chunk = task_refs[:CHUNK_SIZE]
            task_refs = task_refs[CHUNK_SIZE:]

            print("Process a chunk!")
            results = ray.get(tasks_chunk)

            for message, quality in results:
                if quality < best_quality:
                    best_quality = quality
                    best_message = message

        if counter > KEY_LIMIT:
            print("Finished the chunks!")
            break



    return best_message, best_quality



if __name__ == "__main__2":
    # keygen(0)

    kh = HistKeyGen(dictionary_string(), 1)
    
    s = set()
    for x in kh:
        s.add(hash(tuple(x)))

    print(len(s))



if __name__ == "__main__":
    # import sys
    # arg = sys.argv[1]

    with open('test2_plaintext.txt', 'r') as f:
        plaintext = f.readline().strip()

    with open('test2_ciphertext.txt', 'r') as f:
        ciphertext = f.readline().strip()
        # ciphertext = f.readline().strip()
    
    message, quality = decrypt(ciphertext)

    print(f"Our guess was {quality} away, where the expected quality is {(len(ciphertext) - len(plaintext)) / len(ciphertext)}")
    print(f"Guess: \n{message}")

    # print(dictionary_words())
    # print(unigram_distribution('lacrosses protectional blistered leaseback assurers'))
    # print(digram_distribution('lacrosses protectional blistered leaseback assurers'))
