import os, random, struct
from Crypto.Cipher import AES
from Crypto import Random
iv = b'\x8b\xb2\xdf\xc8\xe2\x19Z7H>\n\x80wA\x844'
def gen_key():
    BS = 16
    key = os.urandom(BS)
    print("key")
    print(key)
    return key

def pad(s):
    return s + "0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message,key):
    message = pad(message)
    # print(message)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # print(bytes.fromhex(message.encode('utf-8')))
    return iv + cipher.encrypt(message.encode('utf-8'))

def decrypt(key,ciphertext):
    # iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    print(plaintext)
    return plaintext.decode("utf-8").strip("0")


def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open((in_filename), 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunkBytes = infile.read(chunksize)
                chunk = chunkBytes.decode("utf-8")
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk.encode("utf-8")))

def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = 'decrypt.txt'

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)


key = gen_key()
encrypted = encrypt("TestMessage", key)
print(decrypt(key, encrypted))