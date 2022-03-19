def read_dictionary_1(filename = "dictionary_1.txt"):
    candidates = []
    with open(filename, "r") as file:
        for line in file:
            if len(line) > 50:
                candidates.append(line[:-1]) # remove '/n'
    return candidates


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
    candidates = []
    with open("dictionary_1_low_res.txt") as file:
        for line in file:
            candidates.append(line.strip())
    return candidates


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
    return string_difference_helper(a, 0, b, 0)


def string_difference_helper(a, i_a, b, i_b):
    if i_a == len(a):
        return 0
    elif i_b == len(b):
        return 1000
    elif a[i_a] == b[i_b]: # greedily match a character
        return string_difference_helper(a, i_a + 1, b, i_b + 1)
    elif int(a[i_a]) == int(b[i_b]) + 2 or int(a[i_a]) == int(b[i_b]) - 2: # mismatch
        return string_difference_helper(a, i_a, b, i_b + 1)
    else: # try +1/-1 and skipping, return the smaller
        fudge =  string_difference_helper(a, i_a + 1, b, i_b + 1) + 1
        skip = string_difference_helper(a, i_a, b, i_b + 1)
        return min(fudge, skip)


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
          