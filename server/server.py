import sys
import socket
from threading import Thread,Lock

HOST=''
PORT=1234
BUFFER_SIZE=1024

connected_host={}
connected_host_lock=Lock()

class chat_server_handler():
    def __init__(self, conn, addr):
        self.conn=conn
        self.addr=addr

    def client_broadcaster(self,username,state):
        with connected_host_lock:
            for value in connected_host.values():
                address=value['address']
                conn=value['conn']
                if address != self.addr:
                    try:
                        send_message=f"\tserver: {username} is {state} the chat"
                        conn.sendall(send_message.encode())
                    except:
                        print("couldn't proadcast message")

    def start(self):
        user_handler=chat_server_user_handler(self.conn,self.addr)
        user_handler.start()

   
class chat_server_user_handler(chat_server_handler):
    def __init__(self, conn, addr):
        super().__init__(conn, addr)
        self.user_name=None
    
    def user_name_getter_setter(self):
        self.user_name=self.conn.recv(BUFFER_SIZE).decode().strip()
        with connected_host_lock:
            connected_host[self.user_name]={"address":self.addr,"conn":self.conn}
        
    def message_broadcaster(self,message):
        with connected_host_lock:
            for value in connected_host.values():
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
            if self.user_name in connected_host:
                del connected_host[self.user_name]
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
        
            
def main():
    try:
        banner="""
          _______        __  ____                    
         / ___/ /  ___ _/ /_/ __/__ _____  _____ ____
        / /__/ _ \\/ _ `/ __/\\ \\/ -_) __/ |/ / -_) __/
        \\___/_//_/\\_,_/\\__/___/\\__/_/  |___/\\__/_/   
                                                     
                                                 Version: (v0.0.1)  
                                                 Author : pevinkumar                                
        """
        print(banner)
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind((HOST,PORT))
        sock.listen()
        print(f"Server started....\n\t @ {HOST}:{PORT}")
        while True:
            conn,addr=sock.accept()
            chat_handler=chat_server_handler(conn,addr)
            chat_handler_thread=Thread(target=chat_handler.start)
            chat_handler_thread.start()
    except OSError:
        print(f"Could not establish connection.\n{HOST}:{PORT} is Already in use.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutdowning server")
        sys.exit(0)
    finally:
        sock.close()
if __name__=="__main__":
    main()