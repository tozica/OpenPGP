import base64
import json
import re

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric.dsa import DSAPrivateKey, DSAPublicKey
from cryptography.utils import int_to_bytes
from elgamal.elgamal import PrivateKey, PublicKey, Elgamal, CipherText
from rsa.pem import save_pem, load_pem

from key_rings.base_key_ring.private_key_ring import PrivateKeyRing
from utils.des3_utils.des3_utils import bytes_to_int


class ElgamalPrivateKeyRing(PrivateKeyRing):
    private_key_elgamal: PrivateKey
    public_key_elgamal: PublicKey
    private_key_dsa: DSAPrivateKey
    public_key_dsa: DSAPublicKey

    def __init__(self, timestamp, user_id, email, algorithm, key_size, user_name, encrypted_private_key,
                 key_from_password, private_key_elgamal, public_key_elgamal, private_dsa_key) -> None:
        super().__init__(timestamp, user_id, email, algorithm, key_size, user_name, encrypted_private_key,
                         key_from_password)
        self.private_key_elgamal = private_key_elgamal
        self.public_key_elgamal = public_key_elgamal
        self.public_key = self.get_public_key_as_string()
        self.private_key_dsa = private_dsa_key
        self.public_key_dsa = private_dsa_key.public_key()

    def export_public_key(self, path):
        pem_file_path = path + '/' + self.user_name + '_public.pem'
        metadata_file_path = path + '/' + '.metadata'
        metadata = {
            "timestamp": str(self.timestamp),
            "key_id": self.key_id,
            "user_id": self.user_id,
            "email": self.email,
            "algorithm": self.algorithm,
            "user_name": self.user_name,
            "key_size": self.key_size
        }

        with open(metadata_file_path, 'w', encoding='utf-8') as metadata_file:
            json.dump(metadata, metadata_file, ensure_ascii=False, indent=4)

        p = int_to_bytes(self.public_key_elgamal.p, 256)
        y = int_to_bytes(self.public_key_elgamal.y, 256)

        dsa_bytes = self.public_key_dsa.public_bytes(encoding=serialization.Encoding.PEM,
                                                     format=serialization.PublicFormat.SubjectPublicKeyInfo)

        content = save_pem(p + y + dsa_bytes, "ELGAMAL PUBLIC KEY")

        with open(pem_file_path, 'wb') as pem_file:
            pem_file.write(content)

    def export_private_key(self, path):
        pem_file_path = path + '/' + self.user_name + '_private.pem'
        metadata_file_path = path + '/' + '.metadata'
        metadata = {
            "timestamp": str(self.timestamp),
            "key_id": self.key_id,
            "user_id": self.user_id,
            "email": self.email,
            "algorithm": self.algorithm,
            "user_name": self.user_name,
            "key_size": self.key_size,
            "encrypted_private_key": base64.b64encode(self.encrypted_private_key).decode('utf-8'),
            "key_from_password": base64.b64encode(self.key_from_password).decode('utf-8')
        }

        with open(metadata_file_path, 'w', encoding='utf-8') as metadata_file:
            json.dump(metadata, metadata_file, ensure_ascii=False, indent=4)

        p = int_to_bytes(self.public_key_elgamal.p, 256)
        x = int_to_bytes(self.private_key_elgamal.x, 256)
        y = int_to_bytes(self.public_key_elgamal.y, 256)

        dsa_bytes = self.private_key_dsa.private_bytes(encoding=serialization.Encoding.PEM,
                                                       format=serialization.PrivateFormat.PKCS8,
                                                       encryption_algorithm=serialization.NoEncryption())

        content = save_pem(p + y + x + dsa_bytes, "ELGAMAL PRIVATE KEY")

        with open(pem_file_path, 'wb') as pem_file:
            pem_file.write(content)


    @classmethod
    def import_private_key(cls, path):
        file_name = path.split("/")[len(path.split("/")) - 1]
        metadata_file_path = re.sub(file_name, ".metadata", path)

        with open(path, mode='rb') as pem_file:
            public_key_pem_content = pem_file.read()

        with open(metadata_file_path, mode='r') as metadata_file:
            metadata = json.load(metadata_file)

        pem = load_pem(public_key_pem_content, "ELGAMAL PRIVATE KEY")

        p = pem[:256]
        y = pem[256:512]
        x = pem[512:768]
        dsa = pem[768:]

        elgamal_private = PrivateKey(bytes_to_int(p), bytes_to_int(x))
        elgamal_public = PublicKey(bytes_to_int(p), Elgamal.get_g(bytes_to_int(p)), bytes_to_int(y))
        dsa_private = serialization.load_pem_private_key(dsa, None)

        elgamal_key_ring = ElgamalPrivateKeyRing(metadata["timestamp"], metadata["user_id"], metadata["email"],
                                                 metadata["algorithm"], metadata["key_size"], metadata["user_name"],
                                                 metadata["encrypted_private_key"], metadata["key_from_password"],
                                                 elgamal_private, elgamal_public, dsa_private)

        PrivateKeyRing.insert_row(metadata["email"], elgamal_key_ring)

    @classmethod
    def import_public_key(cls, path, metadata, email):
        pass

    def sign_message(self, message):
        return self.private_key_dsa.sign(message, hashes.SHA1())

    def decrypt_session_key(self, encrypted_session_key):
        a = encrypted_session_key[:256]
        b = encrypted_session_key[256:512]

        return Elgamal.decrypt(CipherText(bytes_to_int(a), bytes_to_int(b)), self.private_key_elgamal)

    def get_public_key_as_string(self):
        return self.public_key_elgamal.__str__()
        pass

    def get_private_key_as_string(self):
        return self.private_key_elgamal.__str__()
        pass

    def get_public_key(self):
        return self.public_key_elgamal
        pass

    def get_private_key(self):
        return self.private_key_elgamal
        pass

    def set_public_key(self, public_key):
        self.public_key_elgamal = public_key
        pass

    def set_private_key(self, private_key):
        self.private_key_elgamal = private_key
        pass
