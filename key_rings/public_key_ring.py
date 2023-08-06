import datetime
import decimal
import string


class PublicKeyRing:
    timestamp: datetime
    keyId: int
    publicKey: int
    ownerTrust: decimal
    userId: string
    keyLegitimacy: decimal
    signatures: [decimal]
    signatureTrusts: [decimal]

    def __init__(self, timestamp, keyId, public_key, ownerTrust, userId, keyLegitimacy, signatures,
                 signatureTrusts) -> None:
        super().__init__()
        self.timestamp = timestamp
        self.keyId = keyId
        self.publicKey = public_key
        self.ownerTrust = ownerTrust
        self.userId = userId
        self.keyLegitimacy = keyLegitimacy
        self.signatures = signatures
        self.signatureTrusts = signatureTrusts


publicKeyRing = list()
