import datetime
import string
import uuid


class PrivateKeyRing:
    timestamp: datetime
    keyId: int
    e: int
    d: int
    n: int
    email: string
    algorith: string
    name: string
    keySize: int
    hashedPassword: bytes
    keyId: int
    salt: bytes

    def __init__(self, timestamp, e, d, n, email, algorith, name, key_size, hashed_password, key_id, salt) -> None:
        super().__init__()
        self.timestamp = timestamp
        self.keyId = 0
        self.e = e
        self.d = d
        self.n = n
        self.email = email
        self.algorith = algorith
        self.name = name
        self.keySize = key_size
        self.hashedPassword = hashed_password
        self.keyId = key_id
        self.id = uuid.uuid4()
        self.salt = salt


privateKeyRing = []
