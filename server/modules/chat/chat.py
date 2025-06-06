try:
    import json
    from threading import Event
    from modules import connected_users,connected_host_lock
    from modules.cryptography.cryptographer import CryptoGraphicHandler
    from modules.auth.authenticator import CryptiHubAuthenticator

except ImportError as Ie:
    print(f"Import Error [modules.Chat]: {Ie}")

BUFFER_SIZE=2048

stop_event=Event()

class ChatServerHandler():
    def __init__(self, conn, addr,room_id):
        self.user_name=None
        self.conn=conn
        self.addr=addr
        self.room_id=room_id
        self.cryptographic_handler = CryptoGraphicHandler(password=self.room_id)
        self.authenticator=CryptiHubAuthenticator()

    def user_name_getter_setter(self):
        encrypted_username = self.conn.recv(BUFFER_SIZE).decode().strip()

        self.user_name = self.cryptographic_handler.decrypt_message(encrypted_username)

        with connected_host_lock:
            if self.user_name not in connected_users:
                connected_users[self.user_name]={"address":self.addr,"conn":self.conn}
                return True
            else:
                try:
                    status=json.dumps({"status":"False","message":"Username already exists,Try again with different username"})
                    encrypted_message = self.cryptographic_handler.encrpt_message(status)
                    self.conn.sendall(encrypted_message)
                    return False
                
                except Exception as E:
                    print(f"Unexpected Exception [modules.chat] :{E}")

    def room_authenticator(self):

        encrypted_room_id = self.conn.recv(BUFFER_SIZE).decode().strip()
        decrypted_room_id = self.cryptographic_handler.decrypt_message(encrypted_room_id)

        room_auth_status=self.authenticator.room_authenticator(self.room_id,decrypted_room_id)

        if room_auth_status:
            status=json.dumps({"status":"True","message":"Room authenticated !"})
            encrypted_message = self.cryptographic_handler.encrpt_message(status)
            self.conn.sendall(encrypted_message)
            return True
        else:
            status=json.dumps({"status":"False","message":"Invalid room id"})
            encrypted_message = self.cryptographic_handler.encrpt_message(status)
            self.conn.sendall(encrypted_message)
            return False

    def info_broadcaster(self,username,state):
        with connected_host_lock:
            for value in connected_users.values():
                address=value['address']
                conn=value['conn']
                if address != self.addr:
                    try:
                        status=f"\tserver: {username} is {state} the chat"
                        encrypted_message = self.cryptographic_handler.encrpt_message(status)
                        conn.sendall(encrypted_message)
                    except Exception as E:
                        print(f"couldn't proadcast message [info_brodcaster]: {E}")

    def message_broadcaster(self,message):
        with connected_host_lock:
            for value in connected_users.values():
                address=value['address']
                conn=value['conn']
                if address != self.addr:
                    try:
                        status=f"{self.user_name} :{message}"
                        encrypted_message = self.cryptographic_handler.encrpt_message(status)
                        conn.sendall(encrypted_message)
                        
                    except Exception as E:
                        print(f"couldn't proadcast message [message_brodcaster]: {E}")
    
    def user_remover_from_chat(self):
        with connected_host_lock:
            if self.user_name in connected_users:
                del connected_users[self.user_name]
        self.info_broadcaster(self.user_name,"left")
            
    def user_message_receiver(self):
        while not stop_event.is_set():
            try:
                encrypted_message=self.conn.recv(BUFFER_SIZE).decode().strip().lower()
                decrypted_message = self.cryptographic_handler.decrypt_message(encrypted_message)
                
                if not encrypted_message:
                    break
                if decrypted_message in ["quit","exit"]:
                    break
                else:
                    self.message_broadcaster(decrypted_message)
            except(ConnectionResetError, ConnectionAbortedError, OSError):
                break
        self.user_remover_from_chat()
        self.conn.close()
        
    def start(self):
        status = "connected succecssfully"
        self.conn.sendall(status.encode())
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
                # TODO : Use this below info for logging.           
                #print(f"user:{self.user_name} [{self.addr[0]}] is connected")
                status=json.dumps({"status":"True","message":"Username setted succecssfully,you can chat now !"})
                encrypted_message = self.cryptographic_handler.encrpt_message(status)

                self.conn.sendall(encrypted_message)
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
        
