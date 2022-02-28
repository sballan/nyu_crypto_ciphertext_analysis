import string
import random

# this key was generated using the generate_key() function below. It's used to
# encrypt all the cipher texts in the ciphertext_examples.txt file
encryption_key = [9, 22, 15, 24, 1, 2, 11, 10, 13, 7, 0, 18, 12, 19, 5, 14, 17, 25, 3, 6, 16, 21, 8, 23, 26, 20, 4]


def generate_key():
    """
    Generates a key k[j] that's a sequence of 27 distinct numbers between 0 and 26 where
    'space' is character j for j=0, 'a' is character j for j=1, ..., 'z' is character j, for j=26
    :return: list of 27 distinct numbers
    """
    # List of numbers from 0 to 26
    x = []
    for i in range(27):
        x.append(i)
    key = random.sample(x, 27)
    return key


def pic_random_message():
    """
    Choose a random message from the 5 L-symbol candidate plaintexts in plaintext_dictionary_test1. L = 500.
    :return: a 500 letter plaintext message
    """
    with open("dictionary_1.txt") as f:
        messages = f.readlines()

    random_pointer = random.randrange(5)
    return messages[random_pointer].strip()


def letter_to_number(char):
    """
    Maps a letter to its number equivalent according to position in the English alphabet where:
    space = 0, a = 1, b = 2,...z=26
    :param char: letter
    :return: value between 0 and 26
    """
    if char == " ":
        return 0
    else:
        return ord(char) - 96


def number_to_letter(number):
    """
    Maps a number to its char equivalent according to position in the English alphabet where:
    0 = space, 1 = a, 2 = b...26=z
    :param number: number between 0 and 26
    :return: a lowercase letter or a space
    """
    if number == 0:
        return " "
    else:
        return chr(number + 96)


def encrypt(message, key):
    """
    Encrypts plaintext message with given key as described by encryption algorithm.
    Input: K[26] and message
    :return: ciphertext[L+r]
    """
    ciphertext_pointer = 0
    message_pointer = 0
    numb_random_characters = 0
    prob_of_random_char = .05
    ciphertext = []

    while ciphertext_pointer < len(message) + numb_random_characters:
        coin_value = random.randint(0, 100) / 100
        if prob_of_random_char < coin_value <= 1:
            # substitute the letter with its corresponding value in key[]
            j = letter_to_number(message[message_pointer])
            ciphertext.append(number_to_letter(key[j]))
            message_pointer += 1
        if 0 <= coin_value <= prob_of_random_char:
            # insert a random character
            ciphertext.append(random.sample(string.ascii_lowercase + " ", 1)[0])
            numb_random_characters += 1
        ciphertext_pointer += 1

    return ''.join(ciphertext)


def create_ciphers():
    """
    This function creates a bunch of ciphertexts and writes them to a text file, along with their plaintext messages separated by a tab.
    We can use that for analysis.
    """
    f = open('ciphertext_examples.txt', 'w')
    for i in range(20):
        # plaintext = pic_random_message()
        plaintext = 'blistered pilfers tortoni smeltery trimmings alefs particulate overachiever moonset rotates harshens imagist stuffer lacrosses outflanked twirlier clarence publishable protectional changeover assurers rankness lingua gladding leaseback invalided farcer favouring baldpates glottic outdates proctological unlikely submerse amulets stolonic freaking frizzlers brickyard hyped'
        ciphertext = encrypt(plaintext, encryption_key)
        line = plaintext + '\t' + ciphertext + "\n"
        f.write(line)
    f.close()

# how to create a ciphertext from a random plaintext message and a random key
# plaintext = pic_random_message()
# key = generate_key()
# print(plaintext,'\t', encrypt(plaintext, key))
