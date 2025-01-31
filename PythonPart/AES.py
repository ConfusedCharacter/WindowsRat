from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

class Crypt:
    def __init__(self,key):
        self.key = key

    def encrypt(self,plaintext):
        key = self.key.encode()
        plaintext = plaintext.encode()
        iv = "A+.8(SASD@#^DFAE"
        iv = iv.encode()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        return base64.b64encode(ciphertext).decode('utf-8')


    def decrypt(self,encoded_text):
        key = self.key.encode()
        ciphertext = base64.b64decode(encoded_text)
        iv = "A+.8(SASD@#^DFAE"
        iv = iv.encode()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext.decode('utf-8')

