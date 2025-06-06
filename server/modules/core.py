try:
    import socket
    from threading import Thread,Event
    from datetime import datetime
    from random import randrange
    from hashlib import md5
    from modules import connected_users,connected_host_lock
    from modules.chat.chat import ChatServerHandler
    from modules.command.commands import ServerCommands
    from modules.cryptography.cryptographer import CryptoGraphicHandler

except ImportError as Ie:
    print(f"Couldn't import [Core]: {Ie}")

HOST=''
PORT=1234

stop_event=Event()
server_commands=ServerCommands()

class CryptiHubCore():
    def __init__(self):
        self.cryptographic_handler = None

    def create_socket(self):
        try:
            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            sock.bind((HOST,PORT))
            return sock
        
        except OSError:
            print(f"Could not establish connection.\n{HOST}:{PORT} is Already in use.")
            return   

    def generate_room_uid(self):
        tool_name="CryptiHub"
        current_time=datetime.now()
        random_number=randrange(10000,50000)
        random_salt = str(current_time) + "_" + str(random_number)
        hash_for_room=md5(random_salt.encode())
        room_id=tool_name + "_" + hash_for_room.hexdigest().strip()

        self.connection_handler = CryptoGraphicHandler(password=room_id)

        print(f"Room id for this room : {room_id}")
        return room_id
    
    def server_brodcaster(self,username,state):
        with connected_host_lock:
            for value in connected_users.values():
                conn=value['conn']
                try:
                    send_message=f"\tserver: {username} has been {state} by admin"
                    encrypted_message = self.cryptographic_handler.encrpt_message(send_message)
                    
                    conn.sendall(encrypted_message.encode())
                except:
                    print("couldn't proadcast message")
    
    def connection_handler(self):
        room_id=self.generate_room_uid()
        sock=self.create_socket()
        sock.listen()
        print(f"Server started ( {HOST}:{PORT} ):")
        try:
            while not stop_event.is_set():
                sock.settimeout(1)
                try:
                    conn,addr=sock.accept()
                    chat_handler=ChatServerHandler(conn,addr,room_id)
                    chat_handler_thread=Thread(target=chat_handler.start,daemon=True)
                    chat_handler_thread.start()
                except socket.timeout:
                    continue

        except KeyboardInterrupt:
            print("\nShutdowning server")
            stop_event.is_set()
        
        finally:
            sock.close()

    def main(self):
        connection_handler_thread=Thread(target=self.connection_handler,daemon=True)
        connection_handler_thread.start()
        print("",end="")
        while not stop_event.is_set():
            try:
                cmd=input("# ")
                if cmd == "/help":
                    print(server_commands.help())
                if cmd == "/users":
                    all_users=server_commands.get_all_users(connected_users)
                    if all_users:
                        print(" ")
                        for user in all_users:
                            print("- " + user)
                        print(" ")
                    else:
                        print("  No users in the chat !")
            except KeyboardInterrupt:
                stop_event.set()

    def start(self):
        self.main()

if __name__=="__main__":
    chc=CryptiHubCore()
    chc.start()