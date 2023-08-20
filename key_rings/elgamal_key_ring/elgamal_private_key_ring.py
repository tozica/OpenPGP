import json

from cryptography.utils import int_to_bytes
from elgamal.elgamal import PrivateKey, PublicKey
from rsa.pem import save_pem

from key_rings.base_key_ring.private_key_ring import PrivateKeyRing


class ElgamalPrivateKeyRing(PrivateKeyRing):
    private_key_elgamal: PrivateKey
    public_key_elgamal: PublicKey

    def __init__(self, timestamp, user_id, email, algorithm, key_size, user_name, encrypted_private_key,
                 key_from_password, private_key_elgamal, public_key_elgamal) -> None:
        super().__init__(timestamp, user_id, email, algorithm, key_size, user_name, encrypted_private_key,
                         key_from_password)
        self.private_key_elgamal = private_key_elgamal
        self.public_key_elgamal = public_key_elgamal
        self.public_key = self.get_public_key_as_string()

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

        public_key_pem_content = save_pem(int_to_bytes(self.public_key_elgamal.y), "ELGAMAL PUBLIC KEY")

        with open(pem_file_path, 'wb') as pem_file:
            pem_file.write(public_key_pem_content)
        pass

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
            "key_size": self.key_size
        }
        with open(metadata_file_path, 'w', encoding='utf-8') as metadata_file:
            json.dump(metadata, metadata_file, ensure_ascii=False, indent=4)

        private_key_pem_content = save_pem(int_to_bytes(self.private_key_elgamal.x), "ELGAMAL PRIVATE KEY")

        with open(pem_file_path, 'wb') as pem_file:
            pem_file.write(private_key_pem_content)
        pass
        pass

    @classmethod
    def import_private_key(cls, path):
        return NotImplemented
        pass

    @classmethod
    def import_public_key(cls, path):
        return NotImplemented
        pass

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
