import time
from utils import make_key, decrypt


class ServiceServer:
    def __init__(self, name: str, password: str):
        self.name = name
        self.key = make_key(password)

    def authenticate(self, service_ticket: bytes,
                     session_key_service: str,
                     username: str) -> bool:

        print(f"\n[{self.name.upper()}] Verifying ticket...")

        ticket = decrypt(service_ticket, self.key)

        if time.time() > ticket["expires"]:
            raise PermissionError("Service ticket expired")

        if ticket["username"] != username:
            raise PermissionError("Username mismatch")

        if ticket["service"] != self.name:
            raise PermissionError("Wrong service")

        print(f"[{self.name.upper()}] {username} authenticated successfully")
        print(f"[{self.name.upper()}] Secure session established")
        return True