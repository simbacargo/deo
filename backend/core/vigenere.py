def vigenere(text: str, key: str, encrypt=True):

    result = ''

    for i in range(len(text)):
        letter_n = ord(text[i])
        key_n = ord(key[i % len(key)])

        if encrypt:
            value = (letter_n + key_n) % 1114112
        else:
            value = (letter_n - key_n) % 1114112

        result += chr(value)

    return result
    

def vigenere_encrypt(text: str, key: str):
    return vigenere(text=text, key=key, encrypt=True)


def vigenere_decrypt(text: str, key: str):
    return vigenere(text=text, key=key, encrypt=False)



# Example
# >>> vigenere_encrypt(u"Hello world!", u"Leet1337:)")
# '\x94ÊÑà\xa0Sª¦¬\x95°\x86'

# >>> vigenere_decrypt(u"\x94ÊÑà\xa0Sª¦¬\x95°\x86", u"Leet1337:)")
# 'Hello world!'