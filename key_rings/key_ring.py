import string
from datetime import datetime
from abc import ABC, abstractmethod


class KeyRing(ABC):
    timestamp: datetime
    key_id: int
    public_key: int
    user_id: string
    email: string
    algorithm: string
    key_size: int
    user_name: string

    key_rings = []

    def __init__(self, timestamp, key_id, public_key, user_id, email, algorithm, key_size, user_name):
        self.timestamp = timestamp
        self.key_id = key_id
        self.public_key = public_key
        self.user_id = user_id
        self.email = email
        self.algorithm = algorithm
        self.key_size = key_size
        self.user_name = user_name

    @abstractmethod
    def export_public_key(self, path):
        pass

    @abstractmethod
    def export_private_key(self, path):
        pass

    @abstractmethod
    def get_public_key_as_string(self):
        pass

    @abstractmethod
    def get_private_key_as_string(self):
        pass

    @abstractmethod
    def get_public_key_as_object(self):
        pass

    @abstractmethod
    def get_private_key_as_object(self):
        pass