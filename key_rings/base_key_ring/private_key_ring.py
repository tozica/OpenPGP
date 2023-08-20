import string
import uuid
from abc import ABC, abstractmethod

from key_rings.base_key_ring.key_ring import KeyRing


class PrivateKeyRing(KeyRing, ABC):
    key_id: int
    public_key: string
    encrypted_private_key: string
    key_from_password: bytes

    private_key_ring_by_user = {}

    def __init__(self, timestamp, user_id, email, algorithm, key_size, user_name, encrypted_private_key,
                 key_from_password):
        super().__init__(timestamp, user_id, email, algorithm, key_size, user_name)
        self.key_id = uuid.uuid4().int
        self.encrypted_private_key = encrypted_private_key
        self.key_from_password = key_from_password

    @abstractmethod
    def export_private_key(self, path):
        pass

    @classmethod
    @abstractmethod
    def import_private_key(cls, path):
        pass

    @abstractmethod
    def set_private_key(self, private_key):
        pass

    @abstractmethod
    def get_private_key(self):
        pass

    @abstractmethod
    def get_private_key_as_string(self):
        pass

    @classmethod
    def insert_row(cls, email, key_ring):
        if email in PrivateKeyRing.private_key_ring_by_user:
            PrivateKeyRing.private_key_ring_by_user[email].append(key_ring)
        else:
            PrivateKeyRing.private_key_ring_by_user[email] = [key_ring]
        pass

    @classmethod
    def delete_row(cls, email, key_ring):
        if email in PrivateKeyRing.private_key_ring_by_user:
            PrivateKeyRing.private_key_ring_by_user[email].remove(key_ring)
            if len(PrivateKeyRing.private_key_ring_by_user[email]) == 0:
                del PrivateKeyRing.private_key_ring_by_user[email]
        pass

    @classmethod
    def delete_user(cls, email):
        if email in PrivateKeyRing.private_key_ring_by_user:
            del PrivateKeyRing.private_key_ring_by_user[email]
