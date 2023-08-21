import json
import re

from cryptography.utils import int_to_bytes
from elgamal.elgamal import Elgamal, CipherText
from elgamal.elgamal import PublicKey
from rsa.pem import load_pem

from key_rings.base_key_ring.public_key_ring import PublicKeyRing
from utils.des3_utils.des3_utils import bytes_to_int


class ElgamalPublicKeyRing(PublicKeyRing):
    public_key_elgamal: PublicKey

    def __init__(self, timestamp, user_id, email, algorithm, key_size, user_name, key_id,
                 public_key_elgamal) -> None:
        super().__init__(timestamp, user_id, email, algorithm, key_size, user_name, key_id)
        self.public_key_elgamal = public_key_elgamal
        self.public_key = self.get_public_key_as_string()

    def export_public_key(self, path):
        pass

    def encrypt_session_key(self, session_key):
        ct: CipherText = Elgamal.encrypt(session_key, self.public_key_elgamal)

        return int_to_bytes(ct.a, 256) + int_to_bytes(ct.b, 256)

    @classmethod
    def import_public_key(cls, path, metadata, email):
        file_name = path.split("/")[len(path.split("/")) - 1]
        metadata_file_path = re.sub(file_name, ".metadata", path)

        with open(path, mode='rb') as pem_file:
            public_key_pem_content = pem_file.read()

        with open(metadata_file_path, mode='r') as metadata_file:
            metadata = json.load(metadata_file)

        pem = load_pem(public_key_pem_content, "ELGAMAL PUBLIC KEY")

        p = pem[:256]
        y = pem[256:512]

        elgamal_public = PublicKey(bytes_to_int(p), Elgamal.get_g(bytes_to_int(p)), bytes_to_int(y))

        elgamal_key_ring = ElgamalPublicKeyRing(metadata["timestamp"], metadata["user_id"], metadata["email"],
                                                metadata["algorithm"], metadata["key_size"], metadata["user_name"],
                                                metadata["key_id"], elgamal_public)

        PublicKeyRing.insert_row(email, elgamal_key_ring)

    def get_public_key_as_string(self):
        return self.public_key_elgamal.__str__()

    def get_public_key(self):
        return self.public_key_elgamal

    def set_public_key(self, public_key):
        self.public_key_elgamal = public_key
