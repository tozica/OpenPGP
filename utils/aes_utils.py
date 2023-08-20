from random import randbytes

from Cryptodome.Cipher import AES


def aes_encrypt(message):
    key = randbytes(16)
    cipher = AES.new(key, AES.MODE_CFB,  bytes(16))
    cipher_text = cipher.encrypt(message.encode("utf8"))
    return key, cipher_text


def aes_decrypt(key, cipher_text):
    cipher = AES.new(key, AES.MODE_CFB,  bytes(16))
    return cipher.decrypt(cipher_text)

