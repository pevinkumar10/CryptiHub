try:
    import json
    from threading import Event
    from modules import connected_users,connected_host_lock
    from modules.cryptography.cryptographer import CryptoGraphicHandler
    from modules.auth.authenticator import CryptiHubAuthenticator

except ImportError as Ie:
    print(f"Import Error [modules.Chat.import]: {Ie}")

BUFFER_SIZE=4096

stop_event=Event()

class ChatServerHandler:
    def __init__(self, conn: object, addr: tuple,room_id: str) -> None:
        """
            Initialize the CryptoGraphicHandler with a password.

            Args:
                conn (socket): The socket connection object.
                addr (tuple): The address of the connected client.
                room_id (str): The unique identifier for the chat room.

            Returns:
                None
        """
        self.user_name = None
        self.conn = conn
        self.addr = addr
        self.room_id = room_id

        self.cryptographic_handler = CryptoGraphicHandler(password = self.room_id)
        self.authenticator = CryptiHubAuthenticator()

    def user_name_getter_setter(self) -> bool:
        """
            Function to get and set the username for the chat.

            Args:
                None

            Returns:
                bool: True if username is set successfully, False otherwise.
        """
        encrypted_username = self.conn.recv(BUFFER_SIZE).decode().strip()

        self.user_name = self.cryptographic_handler.decrypt_message(encrypted_username)

        with connected_host_lock:
            if self.user_name not in connected_users:
                connected_users[self.user_name] = {"address":self.addr,"conn":self.conn}
                return True
            else:
                try:
                    status = json.dumps({"status":"False","message":"Username already exists,Try again with different username"})
                    encrypted_message = self.cryptographic_handler.encrpt_message(status)
                    self.conn.sendall(encrypted_message)
                    return False
                
                except Exception as E:
                    print(f"Unexpected Exception [modules.chat.username] :{E}")

    def room_authenticator(self) -> bool:
        """
            Function to authenticate the room using the room id.

            Args:
                None

            Returns:
                bool: True if the room is authenticated ,Flase if not authenticated.
        
        """
        encrypted_room_id = self.conn.recv(BUFFER_SIZE).strip()

        decrypted_room_id = self.cryptographic_handler.decrypt_message(encrypted_room_id)

        room_auth_status=self.authenticator.room_authenticator(self.room_id,decrypted_room_id)

        if room_auth_status:
            status = json.dumps({"status":"True","message":"Room authenticated !"})
            encrypted_message = self.cryptographic_handler.encrpt_message(status)
            self.conn.sendall(encrypted_message)
            return True
        else:
            status = json.dumps({"status":"False","message":"Invalid room id"})
            encrypted_message = self.cryptographic_handler.encrpt_message(status)
            self.conn.sendall(encrypted_message)
            return False

    def info_broadcaster(self, username: str, state: str) -> None:
        """
        Function to broadcast user information to all connected users.

        Args:
            username (str): The username of the user whose information is being broadcasted.
            state (str): The state of the user (e.g., "joined", "left").
            
        Returns:
            None
        """
        with connected_host_lock:
            users_copy = list(connected_users.items()) 
            
        for user, data in users_copy:
            address = data['address']
            conn = data['conn']
            
            if address == self.addr:
                continue
                
            try:
                if getattr(conn, '_closed', False):
                    continue
                    
                status = f"server: {username} is {state} the chat"
                
                encrypted_message = self.cryptographic_handler.encrpt_message(status)

                conn.settimeout(2.0)
                conn.sendall(encrypted_message)
                
            except (ConnectionError, OSError) as e:
                print(f"[Broadcast error] To {user}@{address}: {e}")
                # Clean up dead connection
                with connected_host_lock:
                    if user in connected_users:
                        del connected_users[user]
            except Exception as e:
                print(f"[Unexpected broadcast error] To {user}@{address}: {e}")

    def message_broadcaster(self,message:str) -> None:
        """
        Function to broadcast user messages to all connected users.

        Args:
            Message (str): User chat message to broadcast.

        Returns:
            None
        """
        with connected_host_lock:
            for value in connected_users.values():
                address = value['address']
                conn = value['conn']
                if address != self.addr:
                    try:
                        status = f"{self.user_name} :{message}"
                        encrypted_message = self.cryptographic_handler.encrpt_message(status).strip()
                        conn.sendall(encrypted_message)
                        
                    except Exception as E:
                        print(f"couldn't proadcast message [message_brodcaster]: {E}")
    
    def user_remover_from_chat(self) -> None:
        """
        Function to remove user from the chat.
        
        Args:
            None

        Returns:
            None
        """
        try:
            with connected_host_lock:
                if self.user_name in connected_users:
                    del connected_users[self.user_name]

            self.info_broadcaster(self.user_name, "left")
        except Exception as e:
            print(f"[Removal error] for {self.user_name}: {e}")
            
    def user_message_receiver(self) -> None:
        """
        Function to receive user messages from all connected users.

        Args:
            None

        Returns:
            None
        """
        while not stop_event.is_set():
            try:
                encrypted_message = self.conn.recv(BUFFER_SIZE).decode().strip()
                if not encrypted_message:
                    break

                decrypted_message = self.cryptographic_handler.decrypt_message(encrypted_message)
                
                if decrypted_message.lower() == "exit":
                    break

                self.message_broadcaster(decrypted_message)

            except(ConnectionResetError, ConnectionAbortedError, OSError):
                pass

        self.user_remover_from_chat()

        try:
            self.conn.close()

        except Exception:
            pass
        
    def start(self) -> None:
        """
        Function to start chat server.
        
        Args:
            None

        Returns:
            None
        """
        status = "Connected succecssfully"
        self.conn.sendall(status.encode())
        try:
            for attempt in range(1,4):
                room_authenticaor_status=self.room_authenticator()
                if room_authenticaor_status:
                    break
            
            if room_authenticaor_status:
                while True:
                    username_set_result=self.user_name_getter_setter()
                    if username_set_result:
                        break
                # TODO : Use this below info for logging.           
                #print(f"user:{self.user_name} [{self.addr[0]}] is connected")
                status = json.dumps({"status":"True","message":"Username setted succecssfully,you can chat now !"})
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
            print(f"Unexpected Exception [modules.chat.start]: {E}")

        finally:
            self.conn.close()
        
