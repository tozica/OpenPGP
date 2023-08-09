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
        pass

    def export_private_key(self, path):
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