# Project 1

**Grading and Submission Policies:** Project 1 will contribute to the class grade as specified in the syllabus. All students must submit for Project 1 using the appropriate link in the Assignments website area, and using the submission naming convention specified below. If you want just one group member to submit your long submission, the other team members have to submit some text or file with a pointer to the submitting student in their team.

The project should be realized by a team of, ideally, 2 or 3 students (well motivated exceptions for 1-person or 4-person teams will be likely accepted). Each team has to detail which tasks were done by which student. The implementation can be in any programming language, but it is recommended to use C or C++, as these are the most recommended (for combined performance and user convenience) programming languages to implement cryptography solutions in the real world. The project comes with a minimal assignment and requires a submission of both software and a report being graded mainly by the TA according to scoring criteria defined below; any additional work you perform might be considered extra credit work if later also submitted under the appropriate space for Extra Credit in the "Quizzes" website area.  

## Project 1 (Cryptanalysis of a class of ciphers):

This cryptanalysis project consists of a software implementation of an algorithm that tries to decrypt an L-symbol challenge ciphertext computed using a specific cipher. Informally speaking, your program's goal is to find the plaintext used to compute this ciphertext within a reasonable amount of time. Specifically, your program should:

print on screen something like `Enter the ciphertext:`,
obtain the ciphertext from `stdin`,
apply some cryptanalysis strategy and
output on screen something like `My plaintext guess is:` followed by the plaintext found by your strategy.

In its cryptanalysis strategy, your program is allowed access to:

- The ciphertext (to be taken as input from `stdin`).
- A plaintext dictionary (to be posted on top of this web page), containing a number `q` of plaintexts, each one obtained as a sequence of space-separated words from the English dictionary
- Partial knowledge of the encryption algorithm used (to be described below).

In its cryptanalysis strategy, your program is not allowed access to:

- The key used by the cipher.
- Part of the encryption scheme (to be detailed below).

The plaintext is a space-separated sequence of words from the English dictionary; thus, each symbol is either a space or one of the 26 lower-case letters from the English alphabet and cannot be a special character, punctuation symbol or upper-case letter; the sentence may not be meaningful, for sake of simplicity.

The key is a sequence of 27 distinct numbers between 0 and 26.  

The ciphertext looks like a sequence of symbols from `{<space>,a,..,z}`.

A text file `plaintext_dictionary_test1` containing a number u of L-symbol candidate plaintexts will be provided to you (as an attachment at the top of this page), and you should feel free to use its content as part of your code.

A text file `plaintext_dictionary_test2` containing a number v of English words will be provided to you (as an attachment at the top of this page), and you should feel free to use its content as part of your code.

Your program will be run using different parameters (e.g., L=500, u=5, v=40; note that these numbers are tentative and may slightly change), and on a number of challenge ciphertexts, each computed using a potentially different variant of the encryption scheme.

Your program should return as output a guess for which L-symbol plaintext was encrypted.

Each ciphertext will be computed from a plaintext selected in one of the following two ways:

- randomly and independently choosing one of the L-symbol plaintexts in `Dictionary1`, or
- concatenating words randomly and independently chosen from `Dictionary2 (any two words being separated by a space, until one has an L-symbol plaintext).

All the encryption schemes used have the following common features:

- The message space is the set {<space>,a,..,z}^L. In other words the message m can be written as m[1],...,m[L], where each m[i] is in {<space>,a,..,z}.
-  The ciphertext space is the set {<space>,a,..,z}^{L+r}, for some r>=0. In other words the the ciphertext c can be written as c[1],...,c[L+r], where each c[i] is in {<space>,a,..,z}.
- The key space is the set of all possible permutations of the set {0,..,26}. In other words the key k can be written as k[0],...,k[26], where each k[j] is in {0,..,26}, for j=1,..,t, and all values k[0],...,k[26] are distinct.
- The encryption algorithm computes the next ciphertext symbol c[i] from the next message symbol m[i'] in two possible ways:
  - as a random value in {<space>,a,..,z}, the idea being that of including a random value in the ciphertext to confuse the eavesdropper
   - as the permuted value of m[i'], where the permutation of each m(i') is chosen using key k, as follows: if m[i'] is = character j, then ciphertext symbol c[i] is equal to k[j], for j=0,...,26 (here, 'space' is character j for j=0, 'a' is character j for j=1, ..., 'z' is character j, for j=26). In other words, each ciphertext symbol c[i] is the permutation of plaintext symbol m[i'] using the appropriate key symbol, which symbol being chosen according to the position of m[i'] into the extended English alphabet {space,a,...,z}. Note that i (the ciphertext position pointer) and i' (the message position pointer) will be more and more different as more random ciphertext symbols are inserted in the ciphertext. 
- which of these two ways happens is left unspecified and and may depend on i',L. In other words, whether the ciphertext symbol is a permuted plaintext symbol or just a random value is being chosen according to an undisclosed, and not key-based, "coin generation" algorithm that is a function of i' and L, and returns a coin value in [0,1] which is compared with a pre-set parameter, called prob_of_random_ciphertext

A pseudocode description of the encryption algorithm could go as follows:
   
```
 Input: key k=k[0],...,k[26] and message m=m[1],...,m[L]
    Instructions:
        ciphertext_pointer = 1 
        message_pointer = 1
        num_rand_characters = 0
        prob_of_random_ciphertext = 0.05 // this value is just an example; we will test your submission with increasing values from 0, 0.05 to (tentatively) 0.75
        Repeat
            let coin_value = coin_generation_algorithm(ciphertext_pointer,L)  // coin_value is a real number in [0,1]
            if prob_of_random_ciphertext < coin_value <= 1 then
                set j = m[message_pointer] // j is a value between 0 and 26
                set c[ciphertext_pointer] = k[j]  
                message_pointer = message_pointer + 1
            if 0 <= coin_value <= prob_of_random_ciphertext then
                randomly choose a character c from {<space>,a,..,z}
                set c[ciphertext_pointer] = c
                num_rand_characters = num_rand_characters + 1
            ciphertext_pointer = ciphertext_pointer +1   
        Until ciphertext_pointer > L + num_rand_characters
        Return c[1]...c[L + num_rand_characters]
```
Note that, for instance, the mono-alphabetic substitution cipher in Lecture 1 is a particular example of this cipher where no random ciphertext symbols are introduced in the ciphertext.

Your program will be scored based on two tests.

- In the first test, your program will be run a few times (e.g., 10), each time on a new ciphertext, computed using the above encryption scheme and a plaintext randomly chosen from the plaintext_dictionary_test1, and a potentially different choice of the prob_of_random_ciphertext, the coin generation algorithm. In this test we will likely choose L=500, and a plaintext dictionary with u=5 plaintexts; these parameter values are tentative and might slightly change.

- In the second test, your program will be run a few times (e.g., 10), each time on a new ciphertext, computed using a plaintext obtained as a space-separate sequence of words that are randomly chosen from a subset of the set of all English words (specifically, a few words randomly taken from word_dictionary_test2) and the above encryption scheme, and a potentially different choice of the prob_of_random_ciphertext, the key character scheduling algorithm and the coin generation algorithm. In this test we will likely choose L=500 and v=40 words; these parameter values are tentative and might slightly change.

To test your strategy, you may use a random coin generation algorithm (i.e., returning a random value in [0,1]) and increasing values for prob_of_random_ciphertext (e.g., 0.05, 0.10, 0.15, etc).

Your executable file should be named "<last name1>-<last name2>-<last name3>-decrypt" (assuming a 3-person team here). Upon execution, it should obtain the ciphertext from stdin, and finally return the output plaintext on stdout within x minutes (or else it will be declared to default to an incorrect guess); most likely, we will choose x = 1 on test 1 and x = 3 on test 2.

If you want to propose more than one cryptanalysis approach, you need to clarify that in your report, and each of your approaches will be tested. You cannot pick more than one approach per team member. Your overall team score will be an average across the success of the various approaches.

Your accompanying report should at least include the following sections:

 1. title of your project (based on your approach); something like "Cryptanalysis of a class of ciphers based on (...)"; the symbol (...) should be replaced with an expression summarizing the main idea(s) in your approach

 2. an introduction containing the team member names; the list of project tasks performed by each student in the team; the number of cryptanalysis approaches you are submitting; and all modifications (if any) you made with respect to the above specifications

 3. a detailed informal explanation (using much more English than pseudo-code) of the cryptanalysis approach or approaches used in your program

 4. a detailed rigorous description (using much more pseudo-code than English) of the cryptanalysis approach or approaches used in your program

Allowed extensions (to be considered as extra credit) include any one among the following:

- if you think your cryptanalysis strategy works well (meaning, it quickly finds the plaintext from the ciphertext) for test1 and the given dictionary_1 file, try increasing the number of candidate plaintexts in this file and see if your strategy still works well, possibly relaxing the restriction on x minutes of running time; report the number (of candidate plaintexts in this file) when you note a large increase in your strategy's running time for each prob_of_random_ciphertext value in 0, 0.1, 0.2, 0.3, 0.4, 0.5, etc., until your strategy works; ideally, reporting pictures showing the runtime as a function of the number of candidate plaintexts in this file;
- similar to (1), but for test2; specifically: if you think your cryptanalysis strategy works well (meaning, it quickly finds the plaintext from the ciphertext) for test2 and the given dictionary_2 file, try increasing the number of words in this file and see if your strategy still works well, possibly relaxing the restriction on x minutes of running time; report the number (of words in this file) when you note a large increase in your strategy's running time for each prob_of_random_ciphertext value in 0, 0.1, 0.2, 0.3, 0.4, 0.5, etc.,; ideally, reporting pictures showing the runtime as a function of the number of words in this file.

Your submission can be a zip file or a link to a github repository, either one posted on this website, under Assignments.

Either of the two must contain at least the following files:

- project report (in pdf form)
- source
- binary.

All of these files (including any requirements.txt file) need to be in the top directory (as opposed in some subdirectory).

You must name your zip file as (assuming a team of 3 students here): <last-name1><last-name2><last-name3>-cs6903s22project1 and your contained files as

`<last-name1><last-name2><last-name3>-report`
`<last-name1><last-name2><last-name3>-decrypt-source`
`<last-name1><last-name2><last-name3>-decrypt-binary`

Your submission will be judged based on the following grading criteria:

- software correctness and usability (i.e., if you followed all of the above instructions, if software runs correctly, and is easy to use)
- quality of report (i.e., how well written is your report)
- cryptanalysis success (i.e., how many challenge ciphertexts your program successfully decrypted). If there are two or more submissions successfully decrypting the same number of challenge ciphertexts, we may rank them based on their (faster to slower) running time taken to produce their outputs.

A good cryptanalysis strategy not guessing any plaintext or an uninteresting cryptanalysis strategy guessing all plaintexts in the first test will be rewarded with a score around the B or B+ level. A good cryptanalysis strategy guessing all plaintexts in the first test will be rewarded with a score around the A- level. Mild success in the second test should be enough for a score in the A level.

The top team(s) will be announced and rewarded with extra credit.

Due date is on the syllabus. No late submissions can be accepted without score penalty and early submissions are encouraged. You are strongly recommended to submit any questions to the TAs (see Syllabus content area for their contact info) and the instructor.
