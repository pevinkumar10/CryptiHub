try:
    import json
    from threading import Event,Lock
    from modules.auth.authenticator import CryptiHubAuthenticator

except ImportError as Ie:
    print(f"Error [modules.Chat]: {Ie}")

BUFFER_SIZE=2048

connected_host_lock=Lock()
connected_hosts={}
stop_event=Event()

#TODO list :-
#   -> Add room authentication                                              ✓
#   -> Add /basic cmds like /kick , /users ,/ban ,/unban ,/help to server
#   -> Username should be unique.                                           ✓
#   -> Use curses for simple GUI
#   -> Exchange keys between clien and server before chat.
#   -> Encrypt the data before send. 


class ChatServerHandler():
    def __init__(self, conn, addr,room_id):
        self.user_name=None
        self.conn=conn
        self.addr=addr
        self.room_id=room_id
        self.authenticator=CryptiHubAuthenticator()

    def user_name_getter_setter(self):
        self.user_name=self.conn.recv(BUFFER_SIZE).decode().strip()
        with connected_host_lock:
            if self.user_name not in connected_hosts:
                connected_hosts[self.user_name]={"address":self.addr,"conn":self.conn}
                return True
            else:
                try:
                    status=json.dumps({"status":"False","message":"Username already exists,Try again with different username"})
                    self.conn.sendall(status.encode())
                    return False
                
                except Exception as E:
                    print(f"Unexpected Exception [modules.chat] :{E}")

    def room_authenticator(self):
        room_id=self.conn.recv(BUFFER_SIZE).decode().strip()
        room_auth_status=self.authenticator.room_authenticator(self.room_id,room_id)
        if room_auth_status:
            status=json.dumps({"status":"True","message":"Room authenticated successfully !"})
            self.conn.sendall(status.encode())
            return True
        else:
            status=json.dumps({"status":"False","message":"Invalid room id"})
            self.conn.sendall(status.encode())
            return False

    def info_broadcaster(self,username,state):
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
        self.info_broadcaster(self.user_name,"left")
            
    def user_message_receiver(self):
        while not stop_event.is_set():
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
        self.conn.sendall("connected succecssfully".encode())
        try:
            # Room Atuthentication started.
            for attempt in range(1,4):
                room_authenticaor_status=self.room_authenticator()
                if room_authenticaor_status:
                    break
            
            # Username configuration started.
            if room_authenticaor_status:
                while True:
                    username_set_result=self.user_name_getter_setter()
                    if username_set_result:
                        break

                print(f"user:{self.user_name} [{self.addr[0]}] is connected")
                status=json.dumps({"status":"True","message":"Username setted succecssfully,you can chat now !"})
                self.conn.sendall(status.encode())
                self.info_broadcaster(self.user_name,"joined")
                self.user_message_receiver()
            else:
                self.conn.close()
        except BrokenPipeError:
            pass
            # TODO : Use this below info for logging.
            # Client {self.addr} Left in room id verification stage 

        except Exception as E:
            print(f"Unexpected Exception [modules.chat]: {E}")

        finally:
            self.conn.close()
        
