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
        key = urlsafe_b64encode(kdf.derive(self.password.encode()))
        fernet = Fernet(key)

        encrypted_message=fernet.encrypt(message.encode())
        final_message=salt + encrypted_message

        return b64encode(final_message)
    
    def decrypt_message(self,encrypted_data):
        # Function to decrypt the encrypted data.
        raw_data = b64decode(encrypted_data)
        salt = raw_data[:16]
        encrypted_message = raw_data[16:]

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1200000,
        )
        key = urlsafe_b64encode(kdf.derive(self.password))
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_message)
        return decrypted.decode()
    
class ChatClient:
    def __init__(self, root):
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

    def connect_to_server(self):
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

    def room_verification(self):
        for attempt in range(1, 4):
            room_id = simple_input_popup(self.root, f"Enter room ID (Attempt {attempt})")

            if room_id is None:
                return False
            
            # initalaizing cryptographic handler.
            self.cryptogrphic_handler = CryptoGraphicHandler(password=room_id)

            encrypted_room_id = self.cryptogrphic_handler.encrpt_message(room_id)
            self.sock.sendall(encrypted_room_id)

            encrypted_room_verification_data = self.sock.recv(BUFFER_SIZE).decode()
            decrypted_message = self.cryptogrphic_handler.decrypt_message(encrypted_room_verification_data)

            result = json.loads(decrypted_message)

            self.update_chat(f"\tServer: {result['message']}")
            if result["status"] == "True":
                return True
        return False

    def set_username(self):
        while True:
            username = simple_input_popup(self.root, "Enter your username:")

            # Encrypting username before sending.
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

    def receive_data(self):
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

    def send_message(self):
        send_message = self.entry_field.get().strip()
        if send_message:
            encrypted_message = self.cryptogrphic_handler.encrpt_message(send_message)
            self.sock.sendall(encrypted_message)
            self.entry_field.delete(0, tk.END)

    def update_chat(self, msg):
        self.chat_window.config(state='normal')
        self.chat_window.insert(tk.END, msg + "\n")
        self.chat_window.yview(tk.END)
        self.chat_window.config(state='disabled')

def simple_input_popup(root, prompt):
    input_win = tk.Toplevel(root)
    input_win.title("Input Required")
    input_win.geometry("300x120+100+100")
    input_val = tk.StringVar()

    tk.Label(input_win, text=prompt).pack(pady=10)
    entry = tk.Entry(input_win, textvariable=input_val)
    entry.pack(pady=5)
    entry.focus()

    def close_win():
        input_win.destroy()

    tk.Button(input_win, text="OK", command=close_win).pack()
    root.wait_window(input_win)

    return input_val.get().strip() or None

# Start the GUI app
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()
