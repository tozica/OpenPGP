from des3_utils.des3_utils import derive_key_from_password, generate_salt
from key_rings.private_key_ring import privateKeyRing


def get_private_key_by_id(ring_id):
    for key in privateKeyRing:
        if key.id == ring_id:
            return key
    return None


def get_property_by_value(name, ring):
    if name == 'N':
        return ring.n
    elif name == 'D':
        return ring.d
    return None


def compare_passwords(password, ring):
    hashed = derive_key_from_password(password, ring.salt)

    if ring.hashedPassword == hashed:
        return True
    else:
        return False


def remove_key_by_id(key_id):
    for key in privateKeyRing:
        if key.id == key_id:
            privateKeyRing.remove(key)
            break


def remove_key(key):
    privateKeyRing.remove(key)
