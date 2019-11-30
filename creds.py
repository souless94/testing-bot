# aes 256
from Crypto import Random
from Crypto.Cipher import AES
from cryptoPad import unpad
from cryptoPad import pad
import base64
import os

# reused code for crpytoPad from https://github.com/dlitz/pycrypto/blob/master/lib/Crypto/Util/Padding.py
_ciphertext = os.environ.get('ciphertext')
_aes_key = os.environ.get('aes_key')
import base64
from Crypto.Cipher import AES
from Crypto import Random

class AESCipher:
    def __init__( self, key ):
        self.key = key.encode("utf8")

    # def encrypt( self, raw ):
    #     raw = bytes(raw, 'utf-8')
    #     raw = pad(raw,32)
    #     iv = Random.new().read( AES.block_size )
    #     cipher = AES.new( self.key, AES.MODE_CBC, iv )
    #     return base64.b64encode( iv + cipher.encrypt( raw ) ).decode("utf-8")

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16].decode("utf-8")
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ),32).decode("utf-8") 
# aes_key = "aes_key"
# print(aes_key)
# aescipher = AESCipher(aes_key)
# encrypted="cipher"
# print("---------------")
# decrypted = aescipher.decrypt(encrypted)
# print(decrypted)

aescipher = AESCipher(_aes_key)
token = aescipher.decrypt(_ciphertext)