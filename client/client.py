try:
    import tkinter as tk
    from tkinter import scrolledtext
    import socket
    import json
    from threading import Thread, Event

except ImportError as Ie:
    print(f"Import Error [client]: {Ie}")

HOST = ''
PORT = 1234
BUFFER_SIZE = 1024

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            self.sock.sendall(room_id.encode())
            result = json.loads(self.sock.recv(BUFFER_SIZE).decode())
            self.update_chat(f"\tServer: {result['message']}")
            if result["status"] == "True":
                return True
        return False

    def set_username(self):
        while True:
            username = simple_input_popup(self.root, "Enter your username:")
            self.sock.sendall(username.encode())
            result = json.loads(self.sock.recv(BUFFER_SIZE).decode())
            if result['status'] == "True":
                self.update_chat(f"\tServer: {result['message']}")
                return True
            else:
                continue

    def receive_data(self):
        while not self.stop_event.is_set():
            try:
                message = self.sock.recv(BUFFER_SIZE).decode().strip()
                if not message or message.lower() == "exit":
                    self.stop_event.set()
                    break
                self.update_chat(message)
            except:
                self.stop_event.set()
                break

    def send_message(self):
        msg = self.entry_field.get().strip()
        if msg:
            self.sock.sendall(msg.encode())
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
