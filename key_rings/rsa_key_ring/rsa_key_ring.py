from cryptography.hazmat.primitives import serialization
from rsa import PrivateKey, PublicKey
import json
from key_rings.key_ring import KeyRing


class RSAKeyRing(KeyRing):
    private_key_rsa: PrivateKey
    public_key_rsa: PublicKey

    def __init__(self, timestamp, key_id, public_key, user_id, email, algorithm, key_size, user_name, private_key_rsa,
                 public_key_rsa) -> None:
        super().__init__(timestamp, key_id, public_key, user_id, email, algorithm, key_size, user_name)
        self.private_key_rsa = private_key_rsa
        self.public_key_rsa = public_key_rsa

    def export_public_key(self, path):
        pem_file_path = path + '/' + self.user_name + '_public.pem'
        metadata_file_path = path + '/' + '.metadata'
        metadata = {
            "timestamp": str(self.timestamp),
            "key_id": self.key_id,
            "user_id": self.user_id,
            "algorithm": self.algorithm,
            "user_name": self.user_name,
            "key_size": self.key_size
        }
        with open(metadata_file_path, 'w', encoding='utf-8') as metadata_file:
            json.dump(metadata, metadata_file, ensure_ascii=False, indent=4)

        public_key_pem_content = self.public_key_rsa.save_pkcs1(format="PEM")

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
            "algorithm": self.algorithm,
            "user_name": self.user_name,
            "key_size": self.key_size
        }
        with open(metadata_file_path, 'w', encoding='utf-8') as metadata_file:
            json.dump(metadata, metadata_file, ensure_ascii=False, indent=4)

        private_key_pem_content = self.private_key_rsa.save_pkcs1(format="PEM")

        with open(pem_file_path, 'wb') as pem_file:
            pem_file.write(private_key_pem_content)

        pass

    def get_public_key_as_string(self):
        return self.public_key_rsa.__repr__()
        pass

    def get_private_key_as_string(self):
        return self.private_key_rsa.__repr__()
        pass

    def get_public_key_as_object(self):
        return self.public_key_rsa
        pass

    def get_private_key_as_object(self):
        return self.private_key_rsa
        pass
