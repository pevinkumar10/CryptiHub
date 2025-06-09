try:
    import os
    from base64 import urlsafe_b64encode , b64encode,b64decode
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

except ImportError as Ie:
    print(f"Couldn't import [modules.cryptography]: {Ie}")

class CryptoGraphicHandler:
    """
        Class to handle cryptographic operations.

        Args:
            password (str): Password used for encryption and decryption.

        Returns:
            None
    """
    def __init__(self,password: str) -> None:
        """
            Initialize the CryptoGraphicHandler with a password.

            Args:
                password (str): The password to be used for encryption and decryption.

            Returns:
                None
        """
        self.password = password

    def encrpt_message(self,message: str) ->bytes:
        """
            Function to encrypt the message before broadcasting.

            Args:
                message (str): The message to be encrypted.

            Returns:
                bytes: The encrypted message encoded in base64.
        """
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm = hashes.SHA256(),
            length = 32,
            salt = salt,
            iterations = 1200000,
        )
        key = urlsafe_b64encode(kdf.derive(self.password.encode()))
        fernet = Fernet(key)

        encrypted_message = fernet.encrypt(message.encode())

        return b64encode(salt + encrypted_message)
    
    def decrypt_message(self,encrypted_data:bytes) ->  str:
        """
            Function to decrypt the exfiltrated data.
            
            Args:
                encrypted_data (bytes): The encrypted data to be decrypted.

            Returns:
                str: The decrypted message.
        """
        raw_data = b64decode(encrypted_data)
        salt = raw_data[:16]
        encrypted_message = raw_data[16:]

        kdf = PBKDF2HMAC(
            algorithm = hashes.SHA256(),
            length = 32,
            salt = salt,
            iterations = 1200000,
        )
        key = urlsafe_b64encode(kdf.derive(self.password.encode()))
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_message)
        return decrypted.decode()
    
    