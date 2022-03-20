import string

from functools import wraps
try: #unix
    import sys
    import resource
    resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
    sys.setrecursionlimit(10**4)
except ImportError: #everything else
    import sys
    sys.setrecursionlimit(10**4)


def read_dictionary_1():

    messages = [
        "underwaists wayfarings fluty analgia refuels transcribing nibbled okra buttonholer venalness hamlet praus apprisers presifted cubital walloper dissembler bunting wizardries squirrel preselect befitted licensee encumbrances proliferations tinkerer egrets recourse churl kolinskies ionospheric docents unnatural scuffler muches petulant acorns subconscious xyster tunelessly boners slag amazement intercapillary manse unsay embezzle stuccoer dissembles batwing valediction iceboxes ketchups phonily con",
        "rhomb subrents brasiers render avg tote lesbian dibbers jeopardy struggling urogram furrowed hydrargyrum advertizing cheroots goons congratulation assaulters ictuses indurates wingovers relishes briskly livelihoods inflatable serialized lockboxes cowers holster conciliating parentage yowing restores conformities marted barrettes graphically overdevelop sublimely chokey chinches abstracts rights hockshops bourgeoisie coalition translucent fiascoes panzer mucus capacitated stereotyper omahas produ",
        "yorkers peccaries agenda beshrews outboxing biding herons liturgies nonconciliatory elliptical confidants concealable teacups chairmanning proems ecclesiastically shafting nonpossessively doughboy inclusion linden zebroid parabolic misadventures fanciers grovelers requiters catmints hyped necklace rootstock rigorously indissolubility universally burrowers underproduced disillusionment wrestling yellowbellied sherpa unburnt jewelry grange dicker overheats daphnia arteriosclerotic landsat jongleur",
        "cygnets chatterers pauline passive expounders cordwains caravel antidisestablishmentarianism syllabubs purled hangdogs clonic murmurers admirable subdialects lockjaws unpatentable jagging negotiated impersonates mammons chumminess semi pinner comprised managership conus turned netherlands temporariness languishers aerate sadists chemistry migraine froggiest sounding rapidly shelving maligning shriek faeries misogynist clarities oversight doylies remodeler tauruses prostrated frugging comestible ",
        "ovulatory geriatric hijack nonintoxicants prophylactic nonprotective skyhook warehouser paganized brigading european sassier antipasti tallyho warmer portables selling scheming amirate flanker photosensitizer multistage utile paralyzes indexer backrests tarmac doles siphoned casavas mudslinging nonverbal weevil arbitral painted vespertine plexiglass tanker seaworthiness uninterested anathematizing conduces terbiums wheelbarrow kabalas stagnation briskets counterclockwise hearthsides spuriously s"]

    return messages


def get_low_res_plaintext():
    candidates = []
    with open("dictionaries/dictionary_1_low_res.txt") as file:
        for line in file:
            candidates.append(line.strip())
    return candidates


def frequency(str):
    freq = {}
    for char in string.ascii_lowercase+" ":
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
    freq_sorted = list(freq.keys())
    freq_sorted.sort(reverse=True, key=lambda k: freq[k])
    
    lst0 = "".join(freq_sorted[:5])
    lst1 = "".join(freq_sorted[5:10])
    
    output = []
    for char in str:
        if char in lst0:
            output.append('0')
        elif char in lst1:
            output.append('1')
        else:
            output.append('2')
    return "".join(output)


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


def memoize(function):    
    memo = {}

    @wraps(function)
    def wrapper(*args):
        # add the new key to dict if it doesn't exist already  
        if args not in memo:
            memo[args] = function(*args)
        return memo[args]
    return wrapper


@memoize
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
    candidates = get_low_res_plaintext()
    #print(candidates)
    plaintexts = read_dictionary_1()
    #print(plaintexts)
    ciphertext = reduce_ciphertext_resolution(str)
    #print(ciphertext)
    
    candidate = "No match"
    candidate_low_res = ""
    min_score = 1000
    for i in range(5):
        score = string_difference(candidates[i], ciphertext)
        # print(score)
        if score < min_score:
            candidate = plaintexts[i]
            min_score = score
            
    return candidate


if __name__ == "__main__":
    ciphertext = input()
    print(decrypt(ciphertext))
          