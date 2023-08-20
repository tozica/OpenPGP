from elgamal.elgamal import PublicKey

from key_rings.base_key_ring.public_key_ring import PublicKeyRing


class ElgamalPublicKeyRing(PublicKeyRing):
    public_key_elgamal: PublicKey

    def __init__(self, timestamp, user_id, email, algorithm, key_size, user_name,
                 public_key_elgamal) -> None:
        super().__init__(timestamp, user_id, email, algorithm, key_size, user_name)
        self.public_key_elgamal = public_key_elgamal
        self.public_key = self.get_public_key_as_string()

    def export_public_key(self, path):
        return NotImplemented
        pass

    def encrypt_session_key(self, session_key):
        return NotImplemented
        pass

    @classmethod
    def import_public_key(cls, path, email):
        return NotImplemented
        pass

    def get_public_key_as_string(self):
        return self.public_key_elgamal.__str__()
        pass

    def get_public_key(self):
        return self.public_key_elgamal
        pass

    def set_public_key(self, public_key):
        self.public_key_elgamal = public_key
        pass
