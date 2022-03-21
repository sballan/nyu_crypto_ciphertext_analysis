import decrypt1_simple, decrypt2

if __name__ == "__main__":
    ciphertext = input("Enter ciphertext: ")

    # Check for invalid chars
    for i in ciphertext:
        if i not in " abcdefghijklmnopqrstuvwxyz":
            print ("Char: %s is invalid" %i)

    message, zscore = decrypt1_simple.decrypt(ciphertext, 1)
    if zscore < 3:
        message = decrypt2.decrypt(ciphertext, 2)[0]

    print(message)