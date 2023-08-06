from enum import Enum


class KEY(Enum):
    PRIVATE = 1
    PUBLIC = 2


class ALGORITHM(Enum):
    RSA = 1
    ELGAMAL = 2
