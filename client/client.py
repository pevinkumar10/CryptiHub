try:
    import os
    import json
    import socket
    import tkinter as tk
    from tkinter import scrolledtext
    from threading import Thread, Event
    from base64 import urlsafe_b64encode , b64encode ,b64decode
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

except ImportError as Ie:
    print(f"Couldn't import [modules.cryptography]: {Ie}")

HOST = ''
PORT = 1234
BUFFER_SIZE = 1024

class CryptoGraphicHandler:
    """
        Class to handle cryptographic operations.
        Args:
            password (str): Password used for encryption and decryption.
        Returns:
            None
    """
    def __init__(self,password: str) ->None:
        """
            Initialize the CryptoGraphicHandler with a password.
            Args:
                password (str): The password to be used for encryption and decryption.
            Returns:
                None
        """
        self.password = password

    def encrpt_message(self,message: str) -> bytes:
        """
            Function to encrypt the message before broadcasting.
            Args:
                message (str): The message to be encrypted.
            Returns:
                bytes: The encrypted message encoded in base64.
        """
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1200000,
        )
        raw_key = kdf.derive(self.password.encode().strip())
        key = urlsafe_b64encode(raw_key)
        fernet = Fernet(key)

        encrypted_message=fernet.encrypt(message.encode())
        return b64encode(salt + encrypted_message)
    
    def decrypt_message(self,encrypted_data: bytes) -> str:
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
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1200000,
        )
        raw_key = kdf.derive(self.password.encode().strip())
        key = urlsafe_b64encode(raw_key)
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_message)
        return decrypted.decode()
    
class ChatClient:
    """
        ChatClient class to handle the chat client GUI and communication with the server.
        Args:
            root (tk.Tk): The root window of the tkinter application.
        Returns:
            None
    """
    def __init__(self, root) -> None:
        """
            Initialize the ChatClient with the root window.
            Args:
                root (tk.Tk): The root window of the tkinter application.
            Returns:
                None
        """
        self.root = root
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cryptogrphic_handler = None
        self.stop_event = Event()

        self.root.title("CryptiHub Chat Client")
        self.root.geometry("400x500")

        self.chat_window = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled')
        self.chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry_field = tk.Entry(self.root)
        self.entry_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0), pady=5)
        self.entry_field.bind("<Return>", lambda event: self.send_message())

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=(0, 10), pady=5)

        self.connect_to_server()

    def connect_to_server(self) -> None:
        """
            Function to connetc the client to the Cryptihub server.
            Args:
                None
            Returns:
                None
        """
        try:
            self.sock.connect((HOST, PORT))
            banner = self.sock.recv(BUFFER_SIZE).decode()
            self.update_chat(f"\tServer: {banner}")
            
            if not self.room_verification():
                self.update_chat("Failed room verification.")
                return
            
            if not self.set_username():
                self.update_chat("Failed to set username.")
                return
            
            Thread(target=self.receive_data, daemon=True).start()

        except Exception as e:
            self.update_chat(f"Connection error: {e}")

    def room_verification(self) -> bool:
        """
            Function to verify the room.
            Args:
                None
            Returns:
                bool: True if verified , False if not verified.
        """
        for attempt in range(1, 4):
            room_id = simple_input_popup(self.root, f"Enter room ID (Attempt {attempt})")

            if room_id is None:
                return False

            self.cryptogrphic_handler = CryptoGraphicHandler(password=room_id)

            encrypted_room_id = self.cryptogrphic_handler.encrpt_message(room_id)
            self.sock.sendall(encrypted_room_id)

            encrypted_room_verification_data = self.sock.recv(BUFFER_SIZE)
            decrypted_message = self.cryptogrphic_handler.decrypt_message(encrypted_room_verification_data)

            result = json.loads(decrypted_message)

            self.update_chat(f"\tServer: {result['message']}")
            if result["status"] == "True":
                return True
            
        return False

    def set_username(self) -> bool:
        """
            Function to setup the username.
            Args:
                None
            Returns:
                bool: True if username set ,False if username isn't set.
        """
        while True:
            username = simple_input_popup(self.root, "Enter your username:")
            if username is None or not username.strip():
                self.update_chat("Username cannot be empty. Please try again.")
                continue

            if len(username) > 20:
                self.update_chat("Username is too long. Please enter a username with 20 characters or less.")
                continue

            encrypted_data = self.cryptogrphic_handler.encrpt_message(username)
            self.sock.sendall(encrypted_data)

            encrypted_username_set_status = self.sock.recv(BUFFER_SIZE).decode()
            decrypted_message = self.cryptogrphic_handler.decrypt_message(encrypted_username_set_status)

            result = json.loads(decrypted_message)

            if result['status'] == "True":
                self.update_chat(f"\tServer: {result['message']}")
                return True
            
            else:
                continue

    def receive_data(self) -> None:
        """
            Function to recieve the message.
            Args:
                None
            Returns:
                None
        """
        while not self.stop_event.is_set():
            try:
                encrypted_data = self.sock.recv(BUFFER_SIZE).decode().strip()
                decrypted_message = self.cryptogrphic_handler.decrypt_message(encrypted_data)

                if not decrypted_message or decrypted_message.lower() == "exit":
                    self.stop_event.set()
                    break

                self.update_chat(decrypted_message)

            except:
                self.stop_event.set()
                break

    def send_message(self) -> None:
        """
            Function to send the message.
            Args:
                None
            Returns:
                None
        """
        send_message = self.entry_field.get().strip()
        if send_message:
            if send_message.lower() == "exit":
                self.update_chat("You have exited the chat.")
                self.stop_event.set()
                self.sock.close()
                self.root.quit()
            else:
                self.update_chat(f"You: {send_message}")
                encrypted_message = self.cryptogrphic_handler.encrpt_message(send_message)
                self.sock.sendall(encrypted_message)
                self.entry_field.delete(0, tk.END)

    def update_chat(self, msg: str) -> None:
        """
            Function to used to update the chat.
            Args:
                msg (str): Message to update in the chat.
            Returns:
                None
        """
        self.chat_window.config(state='normal')
        self.chat_window.insert(tk.END, msg + "\n")
        self.chat_window.yview(tk.END)
        self.chat_window.config(state='disabled')

def simple_input_popup(root, prompt: str) -> str:
    """
        Function to decrypt the exfiltrated data.
        Args:
            root (tk.Tk): The root window of the tkinter application.
            prompt (str): The prompt message to display in the input dialog.
        Returns:
            str: The user input from the dialog, or None if cancelled.
    """
    input_win = tk.Toplevel(root)
    input_win.title("Input Required")
    input_win.geometry("300x120+100+100")
    input_val = tk.StringVar()

    tk.Label(input_win, text=prompt).pack(pady=10)
    entry = tk.Entry(input_win, textvariable=input_val)
    entry.pack(pady=5)
    entry.focus()

    def close_win():
        """
            Function to close the window
            Args:
                None
            Returns:
                None
        """
        input_win.destroy()

    tk.Button(input_win, text="OK", command=close_win).pack()
    root.wait_window(input_win)

    return input_val.get().strip() or None

# Start the GUI app
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()
