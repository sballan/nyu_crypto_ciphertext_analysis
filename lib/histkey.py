import string
from itertools import permutations


class HistKeyGen:
    """
    "Histogram Key Generator".  The HistKey is an array of characters that can be used
    to generate a key given a particular ciphertext.  For a given ciphertext, there is
    a bijection between HistKeys and keys.
    """

    def __init__(self, d_text, tolerance=0, first_chunk_size=0):
        self.d_text = d_text
        self.tolerance = tolerance
        self.first_chunk_size = first_chunk_size

        chunks = self.__create_chunks()

        chunks.reverse()  # This is a funny optimization

        # Each item in `chunk_perms` is an array containing all the permutations for the
        # corresponding chunk in the `chunks` array
        self.chunk_perms = [list(permutations(chunk)) for chunk in chunks]

        # We keep track of which permutation we're considering for each chunk
        self.chunk_ptrs = [0 for _ in chunks]
        # A useful variable for the top of our "stack"
        self.stack_top = len(chunks) - 1
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
                    if self.chunk_ptrs[self.stack_top] < len(
                        self.chunk_perms[self.stack_top]
                    ):
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
                        if (
                            self.chunk_ptrs[self.stack_ptr]
                            < len(self.chunk_perms[self.stack_ptr]) - 1
                        ):
                            self.chunk_ptrs[self.stack_ptr] += 1
                            self.stack_ptr = self.stack_top
                        else:
                            self.chunk_ptrs[self.stack_ptr] = 0
                            self.stack_ptr -= 1
                    else:
                        raise (StopIteration)

            key.reverse()
            return key
        else:
            raise (StopIteration)

    def __iter__(self):
        """Needed to conform to the iterator interface"""
        return self

    def char_distribution(self):
        """
        Character distribution of the dictionary text, as a sorted list of tuples (char, frequency)
        """
        chars = {" ": 0}

        for c in string.ascii_lowercase:
            chars[c] = 0

        for c in self.d_text:
            chars[c] += 1

        # Get the distribution as a list, so we can sort it
        char_dist = list(chars.items())
        # We sort the list by the second item in each tuple, which is the frequency of the
        # character. The result is a list of characters sort from most to least frequent
        char_dist.sort(key=lambda x: x[1], reverse=True)

        return char_dist

    def __create_chunks(self):
        char_dist = self.char_distribution()
        # This chunking procedure groups the characters into arrays where each sequence of characteres
        # has a similar frequency
        chunks = [[]]
        for i, c_t in enumerate(char_dist):
            if len(chunks[-1]) == 0:
                chunks[-1].append(c_t[0])
                continue

            last_freq = char_dist[i - 1][1]          
            if (i <= self.first_chunk_size) or (last_freq - c_t[1]) <= self.tolerance:
                chunks[-1].append(c_t[0])
                continue
            else:
                chunks.append([c_t[0]])
                continue

        return chunks
