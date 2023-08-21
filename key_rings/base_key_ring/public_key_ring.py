import string
from abc import ABC, abstractmethod

from key_rings.base_key_ring.key_ring import KeyRing


class PublicKeyRing(KeyRing, ABC):
    key_id: int
    public_key: string
    owner_trust: int
    key_legitimacy: int
    signature: string
    signature_trust: int

    public_key_ring_by_user = {}

    def __init__(self, timestamp, user_id, email, algorithm, key_size, user_name, key_id):
        super().__init__(timestamp, user_id, email, algorithm, key_size, user_name)
        self.key_id = key_id
        # unclear how to initialize field below
        self.key_legitimacy = 0
        self.owner_trust = 1
        self.signature = ""
        self.signature_trust = 1

    @abstractmethod
    def encrypt_session_key(self, key):
        pass

    @classmethod
    def insert_row(cls, email, key_ring):
        if email in PublicKeyRing.public_key_ring_by_user:
            PublicKeyRing.public_key_ring_by_user[email].append(key_ring)
        else:
            PublicKeyRing.public_key_ring_by_user[email] = [key_ring]
        pass

    @classmethod
    def delete_row(cls, email, key_ring):
        if email in PublicKeyRing.public_key_ring_by_user:
            PublicKeyRing.public_key_ring_by_user[email].remove(key_ring)
            if len(PublicKeyRing.public_key_ring_by_user[email]) == 0:
                del PublicKeyRing.public_key_ring_by_user[email]
        pass

    @classmethod
    def delete_user(cls, email):
        if email in PublicKeyRing.public_key_ring_by_user:
            del PublicKeyRing.public_key_ring_by_user[email]

    @classmethod
    def find_key_by_id(cls, key_id):
        for row, (user, key_rings) in enumerate(PublicKeyRing.public_key_ring_by_user.items()):
            for col, key_ring in enumerate(key_rings):
                if key_ring.key_id == key_id:
                    return key_ring
        return None
        pass
