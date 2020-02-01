import os
from Crypto.Cipher import AES
from Crypto import Random




def gen_key():
    BS = 16
    key = os.urandom(BS)
    return key

def pad(self, s):
    return s + "0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message,key):
    message = pad(message)
    print(message)

    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message.encode('utf8'))

def decrypt(key,ciphertext):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.decode('utf8').strip("0")


