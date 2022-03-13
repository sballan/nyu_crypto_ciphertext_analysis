Leo:
- Problem 2: score our guesses given a key, return the highest score.  Each guess can be calculated in it's own thread for performance.
- We can compare the length of the output string to our known length of 500 chars.
- Generate Alternate Keys: Create a "list of confusion". we can generate alternate keys based on characters that are easily "confused" for one another.  We can score the key based on how "far" it is from our initial guess.
-  


Sammy
- Automated Testing, Prob1, Prob2
- 

Automated Testing:
- Encryption Library: 
  - generate random keys, or keys with specified spaces
  - generate random messages using dictionary 2
  - Encrypt a message given: 1) a key, and 2) a probability for random characters
- Automation
  - Given a key, a message, a ciphertext, run the program and get a score (score is the levenshtein distance between real plaintext and calculated plaintext)
  - Given a range, generate many messages and many keys and many probabilities and test them all

