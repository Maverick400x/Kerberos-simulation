import json
import hashlib
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode


def make_key(password: str) -> bytes:
    """Derive a Fernet key from a password using SHA-256."""
    digest = hashlib.sha256(password.encode()).digest()
    return urlsafe_b64encode(digest)


def encrypt(data: dict, key: bytes) -> bytes:
    return Fernet(key).encrypt(json.dumps(data).encode())


def decrypt(token: bytes, key: bytes) -> dict:
    return json.loads(Fernet(key).decrypt(token).decode())