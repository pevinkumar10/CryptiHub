try:
    import os
    from base64 import urlsafe_b64encode , b64encode
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

except ImportError as Ie:
    print(f"Couldn't import [modules.cryptography]: {Ie}")

class CryptoGraphicHandler:
    def __init__(self,password):
        self.password = password

    def encrpt_message(self,message):
    # Function to encrypt the message before brodcasting.
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1200000,
        )
        key = urlsafe_b64encode(kdf.derive(self.password))
        fernet = Fernet(key)

        encrypted_message=fernet.encrypt(message.encode())
        final_message=salt + encrypted_message

        return b64encode(final_message)