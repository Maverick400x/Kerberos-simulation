from utils import make_key, decrypt


def client_login(kdc, username: str, password: str,
                 service_name: str, service_server):

    print("=" * 55)
    print(f"KERBEROS SIMULATION — User: {username}")
    print("=" * 55)

    user_key = make_key(password)

    # STEP 1 — Get TGT
    tgt, as_response_enc, session_key_tgs = \
        kdc.authentication_server(username)

    as_response = decrypt(as_response_enc, user_key)
    print("[CLIENT] TGS session key received")

    # STEP 2 — Get Service Ticket
    service_ticket, tgs_response_enc, session_key_service = \
        kdc.ticket_granting_server(
            tgt, service_name, session_key_tgs, username
        )

    tgs_response = decrypt(
        tgs_response_enc,
        make_key(session_key_tgs)
    )

    print("[CLIENT] Service session key received")

    # STEP 3 — Access Service
    service_server.authenticate(
        service_ticket,
        session_key_service,
        username
    )