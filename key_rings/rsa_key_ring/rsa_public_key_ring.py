import re
import rsa as rs
from rsa import PublicKey
import json
from key_rings.base_key_ring.public_key_ring import PublicKeyRing


class RSAPublicKeyRing(PublicKeyRing):
    public_key_rsa: PublicKey

    def __init__(self, timestamp, user_id, email, algorithm, key_size, user_name, key_id,
                 public_key_rsa) -> None:
        super().__init__(timestamp, user_id, email, algorithm, key_size, user_name, key_id)
        self.public_key_rsa = public_key_rsa
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

        public_key_pem_content = self.public_key_rsa.save_pkcs1(format="PEM")

        with open(pem_file_path, 'wb') as pem_file:
            pem_file.write(public_key_pem_content)

        pass

    @classmethod
    def import_public_key(cls, path, email):
        pem_file_path = path
        file_name = path.split("/")[len(path.split("/")) - 1]
        metadata_file_path = re.sub(file_name, ".metadata", path)

        with open(pem_file_path, mode='rb') as pem_file:
            public_key_pem_content = pem_file.read()

        public_key_rsa = rs.key.PublicKey.load_pkcs1(public_key_pem_content)

        with open(metadata_file_path, mode='r') as metadata_file:
            metadata = json.load(metadata_file)

        rsa_key_ring = RSAPublicKeyRing(metadata["timestamp"], metadata["user_id"], metadata["email"],
                                        metadata["algorithm"], metadata["key_size"], metadata["user_name"],
                                        metadata["key_id"], public_key_rsa)
        PublicKeyRing.insert_row(email, rsa_key_ring)
        pass

    def get_public_key_as_string(self):
        return self.public_key_rsa.__repr__()
        pass

    def get_public_key(self):
        return self.public_key_rsa
        pass

    def set_public_key(self, public_key):
        self.public_key_rsa = public_key
        pass

