from digitalSignature.Algorithms import modexp
from digitalSignature.GetHash import get_hash
from digitalSignature.KeysGenerator import find_mutually_prime


def encrypt(keys, message):
    intHash = get_hash(message)

    k = find_mutually_prime(keys.p)
    r = modexp(keys.g, k, keys.p)
    l = modexp(k, -1, keys.p - 1) # мультипликативное обратное
    s = l * (intHash - keys.private_key * r) % (keys.p - 1)

    return r, s

def decrypt(keys, r, s, message):
    if not (r > 0 and r < keys.p):
        return False
    if not (s > 0 and s < keys.p - 1):
        return False
    intHash = get_hash(message)

    v1 = pow(keys.public_key, r, keys.p) % keys.p * pow(r, s, keys.p) % keys.p
    v2 = pow(keys.g, intHash, keys.p)

    return v1 == v2
