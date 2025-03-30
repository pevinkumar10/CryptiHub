import socket
from threading import Thread,Event

HOST=''
PORT=1234
BUFFER_SIZE=1024

is_thread_stop=False

def socket_create():
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    return sock

def user_name_set(sock):
    try:
        username=input("Enter your name: ")
        sock.sendall(username.encode())
        return True
    except (OSError,KeyboardInterrupt):
        return False

def receive_data(sock,stop_event):
    while not stop_event.is_set():
        try:
            message=sock.recv(BUFFER_SIZE).decode().strip().lower()
            if message:
                if message[0:7] == "server:":
                    print("\n\t"+message+"\nYou: ",end="")
                else:
                    print("\n"+message+"\nYou: ",end="")
            else:
                stop_event.set()
                break
        except (socket.error,KeyboardInterrupt):
            stop_event.set()
            break
    sock.close()

def main():
    stop_event=Event()
    sock=socket_create()
    try:
        banner="""
          _______        __  ____                    
         / ___/ /  ___ _/ /_/ __/__ _____  _____ ____
        / /__/ _ \\/ _ `/ __/\\ \\/ -_) __/ |/ / -_) __/
        \\___/_//_/\\_,_/\\__/___/\\__/_/  |___/\\__/_/   
                                                     
                                                 Version: (v0.0.1)  
                                                 Author : pevinkumar                                
        """
        sock.connect((HOST,PORT))
        con_msg=sock.recv(BUFFER_SIZE).decode()
        print(banner)
        print(f"\n\tServer: {con_msg}")
        username_set_status_code=user_name_set(sock)
        receive_data_thread=Thread(target=receive_data,args=(sock,stop_event))
        receive_data_thread.start()
        if username_set_status_code:
            while not stop_event.is_set():
                try:
                    send_data=input("").strip()
                    if not send_data:
                        break
                    if send_data not in ["exit","quit"]:
                        sock.sendall(send_data.encode())
                        print("You: ",end="")
                    else:
                        print(send_data)
                        stop_event.set()
                        break
                except KeyboardInterrupt:
                    print("\nQuitted...")
                    break
            sock.send("exit".encode())
                
    except socket.error as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__=="__main__":
    main()