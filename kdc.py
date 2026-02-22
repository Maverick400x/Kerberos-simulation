import os
import time
from base64 import urlsafe_b64encode
from utils import make_key, encrypt, decrypt


class KDC:
    def __init__(self):
        self.users = {
            "alice": "alice_secret",
            "bob": "bob_secret",
            "ranganath":"7801"
        }

        self.services = {
            "fileserver": "fileserver_secret",
            "mailserver": "mailserver_secret",
        }

        self.tgs_key = make_key("kdc_master_secret")

    # STEP 1 — Authentication Server
    def authentication_server(self, username: str) -> tuple:
        if username not in self.users:
            raise ValueError(f"Unknown user: {username}")

        print(f"\n[AS] User '{username}' requesting TGT...")

        user_key = make_key(self.users[username])

        tgt_payload = {
            "username": username,
            "expires": time.time() + 300,
        }

        tgt = encrypt(tgt_payload, self.tgs_key)

        session_key_tgs = urlsafe_b64encode(os.urandom(32)).decode()

        response_to_client = encrypt(
            {"session_key_tgs": session_key_tgs,
             "expires": tgt_payload["expires"]},
            user_key
        )

        return tgt, response_to_client, session_key_tgs

    # STEP 2 — Ticket Granting Server
    def ticket_granting_server(self, tgt: bytes,
                               service_name: str,
                               session_key_tgs: str,
                               username: str) -> tuple:

        if service_name not in self.services:
            raise ValueError(f"Unknown service: {service_name}")

        tgt_data = decrypt(tgt, self.tgs_key)

        if time.time() > tgt_data["expires"]:
            raise PermissionError("TGT expired")

        if tgt_data["username"] != username:
            raise PermissionError("Username mismatch")

        service_key = make_key(self.services[service_name])

        service_ticket_payload = {
            "username": username,
            "service": service_name,
            "expires": time.time() + 120,
        }

        service_ticket = encrypt(service_ticket_payload, service_key)

        session_key_service = urlsafe_b64encode(os.urandom(32)).decode()

        response_to_client = encrypt(
            {"session_key_service": session_key_service,
             "service": service_name},
            make_key(session_key_tgs)
        )

        return service_ticket, response_to_client, session_key_service