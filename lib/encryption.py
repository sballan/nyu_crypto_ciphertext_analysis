import string
import random
import Levenshtein
import os
import csv
import decrypt1
import decrypt2
try: #unix
    import sys
    import resource
    resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
    sys.setrecursionlimit(10**4)
except ImportError: #everything else
    import sys
    sys.setrecursionlimit(10**4)

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
    messages = [
        "underwaists wayfarings fluty analgia refuels transcribing nibbled okra buttonholer venalness hamlet praus apprisers presifted cubital walloper dissembler bunting wizardries squirrel preselect befitted licensee encumbrances proliferations tinkerer egrets recourse churl kolinskies ionospheric docents unnatural scuffler muches petulant acorns subconscious xyster tunelessly boners slag amazement intercapillary manse unsay embezzle stuccoer dissembles batwing valediction iceboxes ketchups phonily con",
        "rhomb subrents brasiers render avg tote lesbian dibbers jeopardy struggling urogram furrowed hydrargyrum advertizing cheroots goons congratulation assaulters ictuses indurates wingovers relishes briskly livelihoods inflatable serialized lockboxes cowers holster conciliating parentage yowing restores conformities marted barrettes graphically overdevelop sublimely chokey chinches abstracts rights hockshops bourgeoisie coalition translucent fiascoes panzer mucus capacitated stereotyper omahas produ",
        "yorkers peccaries agenda beshrews outboxing biding herons liturgies nonconciliatory elliptical confidants concealable teacups chairmanning proems ecclesiastically shafting nonpossessively doughboy inclusion linden zebroid parabolic misadventures fanciers grovelers requiters catmints hyped necklace rootstock rigorously indissolubility universally burrowers underproduced disillusionment wrestling yellowbellied sherpa unburnt jewelry grange dicker overheats daphnia arteriosclerotic landsat jongleur",
        "cygnets chatterers pauline passive expounders cordwains caravel antidisestablishmentarianism syllabubs purled hangdogs clonic murmurers admirable subdialects lockjaws unpatentable jagging negotiated impersonates mammons chumminess semi pinner comprised managership conus turned netherlands temporariness languishers aerate sadists chemistry migraine froggiest sounding rapidly shelving maligning shriek faeries misogynist clarities oversight doylies remodeler tauruses prostrated frugging comestible ",
        "ovulatory geriatric hijack nonintoxicants prophylactic nonprotective skyhook warehouser paganized brigading european sassier antipasti tallyho warmer portables selling scheming amirate flanker photosensitizer multistage utile paralyzes indexer backrests tarmac doles siphoned casavas mudslinging nonverbal weevil arbitral painted vespertine plexiglass tanker seaworthiness uninterested anathematizing conduces terbiums wheelbarrow kabalas stagnation briskets counterclockwise hearthsides spuriously s"]

    random_pointer = random.randrange(5)
    return messages[random_pointer]


def letter_to_number(char):
    """
    Maps a letter to its number equivalent according to position in the English alphabet where:
    space = 0, a = 1, b = 2,...z=26
    :param char: letter
    :return: value between 0 and 26
    """
    if char == " ":
        return 0
    elif char in string.ascii_lowercase:
        return ord(char) - 96
    else:
        raise ValueError('Message letters should be either a space or a lower case letter only. Wrong letter: ' + char)


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


def encrypt(message, key, prob_of_random_char):
    """
    Encrypts plaintext message with given key as described by encryption algorithm.
    Input: K[26] and message
    :param message: Plaintext message to encrypt.
    :param key: Encryption key
    :param prob_of_random_char: Random character probability.
    :return: ciphertext[L+r]
    """
    ciphertext_pointer = 0
    message_pointer = 0
    numb_random_characters = 0
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


def create_ciphers(prob_of_random_char):
    """
    This function creates a number of ciphertexts and writes them to a text file, along with their
    plaintext messages separated by a tab. We can use that for analysis.
    """
    f = open('../ciphertext_examples.txt', 'w')
    for i in range(20):
        plaintext = pic_random_message()
        ciphertext = encrypt(plaintext, encryption_key, prob_of_random_char)
        line = plaintext + '\t' + ciphertext + "\n"
        f.write(line)
    f.close()


# how to create a ciphertext from a random plaintext message and a random key
# plaintext = pic_random_message()
# key = generate_key()
# print(plaintext,'\t', encrypt(plaintext, key))


def create_messages_problem2():
    """
    Creates a 500 char message by randomly choosing words from dictionary_2.txt. Truncates the last word if message
        total length would exceed the 500 limit.
    :return: A 500 char string ( message)
    """
    with open("../dictionary_2.txt") as f:
        lines = f.readlines()
    words = []

    for word in lines:
        words.append(word.strip())

    message = words[random.randrange(len(words))]
    while len(message) <= 500:
        random_word = words[random.randrange(len(words))]
        message = message + " " + random_word

    return message[:500]


def test_decryption_algorithm(decryption_function, test_type=1):
    """
    Tests the performance of a decryption algorithm given multiple ciphertexts for the same plaintext message with
    different keys and different percentages of random characters ( starting from 0, .1, .2, .3 ... 1) and prints out
    metrics and results to a folder. The decryption function should return a guessed plain text message given a
    ciphertext.
    The metric: Levenshtein distance between plain text message & guessed message ( returned by
    decryption_function).

     :param decryption_function: the proposed decryption function(algorithm)
     :param test_type: problem 1 or 2. If not set will choose a random message from either problem 1 or 2.
     :return: prints out average Levenshtein distance on all the tests ( outputs all test results to a folder).
    """

    # Choose a plain text message
    if test_type == 1:
        message = pic_random_message()
    elif test_type == 2:
        message = create_messages_problem2()
    else:
        random_choice = random.randrange(2)
        if random_choice == 0:
            message = pic_random_message()
        else:
            message = create_messages_problem2()

    # Create a folder to save the results
    folder_name = "results_" + str(random.randint(0, 10000))
    print("Results saved in folder: " + folder_name)
    os.makedirs(folder_name)

    # start with zero random char
    random_char_percentage = 0
    while random_char_percentage <= 1:
        # Test the decryption algorithm 5, fix the random char percentage and change the key each time
        output = []
        for i in range(5):
            # Generate a random key and encrypt the message
            key = generate_key()
            ciphertext = encrypt(message, key, random_char_percentage)

            # Decrypt the cipher text with the decryption_function()
            try:
                guessed_message = decryption_function(ciphertext,1)
            except:
                print("Error decrypting the following message:  ")
                print("Ciphertext: " + ciphertext)
                print("Key: " + str(key))
                # iINDICATE A FAILED DECRYPTION ATTEMPT
                guessed_message = 'X' * 500

            # Decrypt the cipher text with the decryption_function()
            # Calculate the Levenshtein distance and save the result
            levenshtein_distance = Levenshtein.distance(message, guessed_message)
            result = dict()
            result["key"] = key
            result["ciphertext"] = ciphertext
            result["guessed_message"] = guessed_message
            result["distance"] = levenshtein_distance
            output.append(result)

        # Save the results of each test to a separate CSV file
        with open(os.path.join(folder_name, 'random_char_prob_' + str(random_char_percentage)[:3] + '.csv'), 'w', newline='') as f:
            # Write the headers
            writer = csv.writer(f)
            headers = ["Distance", "Guessed message", "Ciphertext ", "Key"]
            writer.writerow(headers)
            # Write the results
            for i in output:
                row = [str(i["distance"]), str(i["guessed_message"]), str(i["ciphertext"]), str(i["key"])]
                writer.writerow(row)
            # Write the plaintext message to the CSV file ( for analysis)
            writer.writerow(["0", message])
            # Calculate and print average Levenshtein distance
            average = 0
            for i in range(5):
                average += output[i]["distance"]
            average = average / 5
            text_to_print = "Average Levenshtein distance for random char prob " + str(random_char_percentage)[:3] + " is : " + str(
                average)
            print(text_to_print)
            writer.writerow([text_to_print])

        # increase the random char probability by .1
        random_char_percentage += .1



