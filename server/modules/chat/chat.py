try:
    from modules import connected_hosts,connected_host_lock

except ImportError as Ie:
    print(f"Error [modules.Chat]: {Ie}")
    
BUFFER_SIZE=2048

class ChatServerHandler():
    def __init__(self, conn, addr):
        self.user_name=None
        self.conn=conn
        self.addr=addr
    
    def user_name_getter_setter(self):
        self.user_name=self.conn.recv(BUFFER_SIZE).decode().strip()
        with connected_host_lock:
            connected_hosts[self.user_name]={"address":self.addr,"conn":self.conn}

    def client_broadcaster(self,username,state):
        with connected_host_lock:
            for value in connected_hosts.values():
                address=value['address']
                conn=value['conn']
                if address != self.addr:
                    try:
                        send_message=f"\tserver: {username} is {state} the chat"
                        conn.sendall(send_message.encode())
                    except:
                        print("couldn't proadcast message")

    def message_broadcaster(self,message):
        with connected_host_lock:
            for value in connected_hosts.values():
                address=value['address']
                conn=value['conn']
                if address != self.addr:
                    try:
                        send_message=f"{self.user_name} :{message}"
                        conn.sendall(send_message.encode())
                    except:
                        print("couldn't proadcast message")
    
    def user_remover_from_chat(self):
        with connected_host_lock:
            if self.user_name in connected_hosts:
                del connected_hosts[self.user_name]
        self.client_broadcaster(self.user_name,"left")
            
    def user_message_receiver(self):
        while True:
            try:
                user_message=self.conn.recv(BUFFER_SIZE).decode().strip().lower()
                if not user_message:
                    break
                if user_message in ["quit","exit"]:
                    break
                else:
                    self.message_broadcaster(user_message)
            except(ConnectionResetError, ConnectionAbortedError, OSError):
                break
        self.user_remover_from_chat()
        self.conn.close()
        
    def start(self):
        try:
            self.conn.sendall("connected succecssfully".encode())
            self.user_name_getter_setter()
            print(f"user:{self.user_name} [{self.addr[0]}] is connected")
            self.conn.sendall("Username setted succecssfully\nyou can chat now !".encode())
            self.client_broadcaster(self.user_name,"joined")
            self.user_message_receiver()
        except Exception:
            print("Error")
        finally:
            self.conn.close()
        
