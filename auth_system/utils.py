import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(raw_password: str, stored_hash: str) -> bool:
    return hashlib.sha256(raw_password.encode()).hexdigest() == stored_hash