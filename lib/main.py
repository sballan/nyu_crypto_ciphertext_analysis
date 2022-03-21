from lib import decrypt1_simple, decrypt2
ciphertext = input("Enter ciphertext: ")

# Check for invalid chars
for i in ciphertext:
    if i not in " abcdefghijklmnopqrstuvwxyz":
        print ("Char: %s is invalid" %i)

