try:
    import socket
    from threading import Thread,Event
    from datetime import datetime
    from random import randrange
    from hashlib import md5
    from colorama import Fore,Back,Style
    from modules.chat.chat import ChatServerHandler

except ImportError as Ie:
    print(f"Error [Core]: {Ie}")

HOST=''
PORT=1234

stop_event=Event()

class CryptiHubCore():
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
        room_hash_id=tool_name + "_" + hash_for_room.hexdigest().strip()


        print(f"Room id for this room :{room_hash_id}")
        return room_hash_id
    
    def connection_handler(self):
        room_id=self.generate_room_uid()
        sock=self.create_socket()
        sock.listen()
        print(f"Server started....\n\t @ {HOST}:{PORT}")
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
                cmds=input("Iam echo :")
                print(cmds)

            except KeyboardInterrupt:
                stop_event.set()

    def start(self):
        self.main()

if __name__=="__main__":
    chc=CryptiHubCore()
    chc.start()