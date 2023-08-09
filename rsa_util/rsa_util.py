import rsa as rs
from key_rings.enumerations import KEY


def generate_keys(nbits):
    (publicKey, privateKey) = rs.newkeys(nbits)
    return publicKey, privateKey


def import_from_file(path, keyType):
    with open(path, mode='rb') as file:
        keydata = file.read()
    key = None
    if keyType == KEY.PRIVATE:
        key = rs.key.PrivateKey.load_pkcs1(keydata)
    elif keyType == KEY.PUBLIC:
        key = rs.key.PublicKey.load_pkcs1(keydata)
    return key


# def export_public_to_file(path, key: PrivateKeyRing):
#     public_key = rsa.RSAPublicNumbers(key.e, key.n).public_key()
#
#     pem = public_key.public_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PublicFormat.SubjectPublicKeyInfo
#     )
#
#     with open(path, 'wb') as pem_file:
#         pem_file.write(pem)
