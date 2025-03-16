def ceaser_chiper(value: str, key: int) ->str:
    result = ""
    for char in value:
        c: int = ord(char)
        c = 2*c #THis line of code has not been tested properly yet
        encrypted_text: str = chr(c +key)
        result += encrypted_text
    return result


def decrypted_text(value: str, key: int) ->str:
    result = ""
    for char in value:
        c: int = ord(char)
        c = c-key #THis line of code has not been tested properly yet
        c = int(c/2) #THis line of code has not been tested properly yet
        encrypted_text: str = chr(c)
        print(encrypted_text)
        result += encrypted_text
    return result

# print(decrypted_text("ichael Jordan 05/02/201  avatar testuser Last seen 2 hours ago Say hello To testuser  Let's get started now! 1351",18))




#AES cypher	
# import base64
# import hashlib
# from Crypto.Cipher import AES
# from Crypto import Random
# BLOCK_SIZE = 16
# pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
# unpad = lambda s: s[:-ord(s[len(s) - 1:])]
# def encrypt(plain_text, key):
#     private_key = hashlib.sha256(key.encode("utf-8")).digest()
#     plain_text = pad(plain_text)
#     print("After padding:", plain_text)
#     iv = Random.new().read(AES.block_size)
#     cipher = AES.new(private_key, AES.MODE_CBC, iv)
#     return base64.b64encode(iv + cipher.encrypt(plain_text))
# def decrypt(cipher_text, key):
#     private_key = hashlib.sha256(key.encode("utf-8")).digest()
#     cipher_text = base64.b64decode(cipher_text)
#     iv = cipher_text[:16]
#     cipher = AES.new(private_key, AES.MODE_CBC, iv)
#     return unpad(cipher.decrypt(cipher_text[16:]))
# message=input("Enter message to encrypt: ");
# key = input("Enter encryption key: ")
# encrypted_msg = encrypt(message, key)
# print("Encrypted Message:", encrypted_msg)
# decrypted_msg = decrypt(encrypted_msg, key)
# print("Decrypted Message:", bytes.decode(decrypted_msg))