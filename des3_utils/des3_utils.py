from Cryptodome.Cipher import DES3
import hashlib
from Cryptodome.Random import get_random_bytes


def pad_plaintext(plaintext, block_size):
    padding_len = block_size - len(plaintext) % block_size
    padding = bytes([padding_len] * padding_len)
    return plaintext + padding


def unpad_plaintext(padded_plaintext):
    padding_len = padded_plaintext[-1]
    return padded_plaintext[:-padding_len]


def derive_key_from_password(password, salt, iterations=10000, key_length=24):
    key = hashlib.pbkdf2_hmac('sha512', password.encode(), salt, iterations, dklen=key_length)

    return key


def generate_salt():
    return get_random_bytes(16)


def int_to_bytes(n):
    hex_value = hex(n)[2:]  # Convert the big integer to hexadecimal string
    if len(hex_value) % 2 != 0:
        hex_value = '0' + hex_value
    byte_value = bytes.fromhex(hex_value)  # Convert the hexadecimal string to bytes
    return byte_value


def bytes_to_int(byte_value):
    hex_value = byte_value.hex()  # Convert the bytes to hexadecimal string
    int_value = int(hex_value, 16)  # Convert the hexadecimal string to big integer
    return int_value


def encrypt(plaintext, key):
    cipher = DES3.new(key, DES3.MODE_ECB)
    block_size = DES3.block_size
    padded_plaintext = pad_plaintext(plaintext, block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext


def decrypt(ciphertext, key):
    cipher = DES3.new(key, DES3.MODE_ECB)
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad_plaintext(padded_plaintext)
    return plaintext


def perform_encrypt(d, password):
    plaintext_bytes = int_to_bytes(d)

    salt = generate_salt()
    key = derive_key_from_password(password, salt)

    return key, encrypt(plaintext_bytes, key), salt


def perform_decrypt(encrypt_d, key):
    decrypted_plaintext_bytes = decrypt(encrypt_d, key)
    return bytes_to_int(decrypted_plaintext_bytes)

