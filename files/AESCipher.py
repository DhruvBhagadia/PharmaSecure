import os
from Crypto.Cipher import AES
from Crypto import Random

class AESCipher:
	def __init__(self, key, key_size):
	    self.key = key
	    self.key_size = key_size

	def pad(self, s):
		return s + "0" * (AES.block_size - len(s) % AES.block_size)

	def encrypt(self, message):
	    message = self.pad(message)
	    print(message)
	    iv = Random.new().read(AES.block_size)
	    cipher = AES.new(self.key, AES.MODE_CBC, iv)
	    return iv + cipher.encrypt(message.encode('utf8'))

	def decrypt(self, ciphertext):
	    iv = ciphertext[:AES.block_size]
	    cipher = AES.new(self.key, AES.MODE_CBC, iv)
	    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
	    return plaintext.decode('utf8').strip("0")