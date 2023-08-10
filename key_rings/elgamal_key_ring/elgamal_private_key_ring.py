
from elgamal.elgamal import PrivateKey, PublicKey

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
        return NotImplemented
        pass

    def export_private_key(self, path):
        return NotImplemented
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
