import string
import uuid
from abc import ABC

from key_rings.base_key_ring.key_ring import KeyRing


class PublicKeyRing(KeyRing, ABC):
    key_id: int
    public_key: int
    owner_trust: int
    key_legitimacy: int
    signature: string
    signature_trust: int

    public_key_ring_by_user = {}

    def __init__(self, timestamp, user_id, email, algorithm, key_size, user_name):
        super().__init__(timestamp, user_id, email, algorithm, key_size, user_name)
        self.key_id = uuid.uuid4().int

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