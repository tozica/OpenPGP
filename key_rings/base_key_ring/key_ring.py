import string
from abc import abstractmethod, ABC
from datetime import datetime


class KeyRing(ABC):
    timestamp: datetime
    user_id: string
    email: string
    algorithm: string
    key_size: int
    user_name: string

    def __init__(self, timestamp, user_id, email, algorithm, key_size, user_name):
        self.timestamp = timestamp
        self.user_id = user_id
        self.email = email
        self.algorithm = algorithm
        self.key_size = key_size
        self.user_name = user_name

    @abstractmethod
    def export_public_key(self, path):
        pass

    @classmethod
    @abstractmethod
    def import_public_key(cls, path):
        pass

    @abstractmethod
    def get_public_key_as_string(self):
        pass

    @abstractmethod
    def get_public_key(self):
        pass

    @abstractmethod
    def set_public_key(self, public_key):
        pass
