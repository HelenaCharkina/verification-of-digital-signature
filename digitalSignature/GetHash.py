import hashlib


def get_hash(source):
    return int(hashlib.sha256(source.encode('utf-8')).hexdigest(), 16)

