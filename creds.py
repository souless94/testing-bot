# aes 256
from Crypto import Random
from Crypto.Cipher import AES
from cryptoPad import unpad
import base64
import os

# reused code for crpytoPad from https://github.com/dlitz/pycrypto/blob/master/lib/Crypto/Util/Padding.py
_ciphertext = os.environ.get('ciphertext')
_id = os.environ.get('id')
key_size = [16,24,32] # aes 128,192,256
def aes_decrypt(ciphertext):
    ctxt = base64.b64decode(ciphertext)
    iv = ctxt[:16]
    enc = ctxt[16:]
    aeskey = base64.b64decode(_id)
    cipher = AES.new(aeskey,AES.MODE_CBC,iv)
    plaintext = unpad(cipher.decrypt(enc),32)
    plaintext = plaintext.decode("utf-8")
    return plaintext

token = aes_decrypt(_ciphertext)