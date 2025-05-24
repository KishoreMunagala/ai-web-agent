import keyring

def set_credentials(service: str, username: str, password: str):
    """Store credentials securely using keyring."""
    keyring.set_password(service, username, password)
    print(f"[Credentials] Stored credentials for {service}:{username}")

def get_credentials(service: str, username: str) -> str:
    """Retrieve credentials securely using keyring."""
    password = keyring.get_password(service, username)
    print(f"[Credentials] Retrieved credentials for {service}:{username}")
    return password 