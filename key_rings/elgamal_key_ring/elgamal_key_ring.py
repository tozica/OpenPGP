from elgamal.elgamal import PrivateKey, PublicKey

from key_rings.key_ring import KeyRing


class ElgamalKeyRing(KeyRing):
    private_key_elgamal: PrivateKey
    public_key_elgamal: PublicKey

    def __init__(self, timestamp, key_id, public_key, user_id, email, algorithm, key_size, user_name,
                 private_key_elgamal, public_key_elgamal) -> None:
        super().__init__(timestamp, key_id, public_key, user_id, email, algorithm, key_size, user_name)
        self.private_key_elgamal = private_key_elgamal
        self.public_key_elgamal = public_key_elgamal

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
