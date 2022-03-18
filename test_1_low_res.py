def read_dictionary_1(filename = "dictionary_1.txt"):
    candidates = []
    with open(filename, "r") as file:
        for line in file:
            if len(line) > 50:
                candidates.append(line[:-1]) # remove '/n'
    return candidates


def reduce_candidate_resolution(str):
    """
    Reduce a string to a string of characteristic characters.
    
    The 5 most frequent characters ` esir` will be replaced with `0`
    The next 5 most frequent characters `antol` will be replaced with `1`
    The rest of characters `cugdpbhmykvwfzxjq` will be replaced with `2`
    """
    output = []
    for char in str:
        if char in " esir":
            output.append('0')
        if char in "antol":
            output.append('1')
        if char in "cugdpbhmykvwfzxjq":
            output.append('2')
    return "".join(output)


def frequency(str):
    freq = {}
    for char in string.ascii_lowercase:
        freq[char] = 0
    for char in str:
        freq[char] += 1
    return freq


def reduce_ciphertext_resolution(str):
    """
    Reduce a string to a string of characteristic characters
    
    The 5 most frequent characters will be replaced with `0`
    The next 5 most frequent characters will be ommitted
    The rest of the characters will be replaced with `2`
    """
    freq = frequency(str)
    
    


def get_low_res_plaintext():
    candidates = read_dictionary_1()
    candidates_low_res = []
    for candidate in candidates:
        candidates_low_res.append(reduce_resolution(candidate))
    return candidates_low_res


def is_subsequence(a, b):
    i = 0
    for char in a:
        if i < len(b) and char == b[i]:
            i += 1
    return i == len(b)


def string_difference(a, b):
    """
    Given input strings `a` and `b`, where the length of a is less than or 
    equal to that of b and the alphabet is {0, 1, 2}, this returns the
    "one-way" distance of the two strings such that:
    - the distance is 0 if a is a subsequence of b
    - the distance is the minimum number of +1 or -1 to each individual 
      characters in `a` so that this modified `a` becomes a subsequence of `b`
    
    For example, string_difference("0120", "101121") is 1 since the minimum 
    "edits" to `0120` to be a subsequence of `101121` is for `0120` to become
    `0121`
    """


def decrypt(str):
    candidates = candidates_low_res()
    ciphertext = reduce_resolution(str)
    
    possible_candidates = []
    for i in range(len(candidates)):
        if is_subsequence(candidates[i], ciphertext):
            possible_candidates.append(i)
    return possible_candidates


if __name__ == "__main__":
    ciphertext = input()
    print(decrypt(ciphertext))
          