try:
    import sys
    import socket
    from colorama import Fore,Back,Style
    from threading import Thread
    from modules import Host,Port
    from modules.chat.chat import ChatServerHandler

except ImportError as Ie:
    print(f"Error [Core]: {Ie}")

class CryptiHubCore():
    def create_socket(self):
        try:
            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            sock.bind((Host,Port))
            return sock
        except OSError:
            print(f"Could not establish connection.\n{Host}:{Port} is Already in use.")
            sys.exit(1)    
    
    def main(self):
        sock=self.create_socket()
        sock.listen()
        print(f"Server started....\n\t @ {Host}:{Port}")
        try:
            while True:
                conn,addr=sock.accept()
                chat_handler=ChatServerHandler(conn,addr)
                chat_handler_thread=Thread(target=chat_handler.start)
                chat_handler_thread.start()

        except KeyboardInterrupt:
            print("\nShutdowning server")
            sys.exit(0)

    def start(self):
        self.main()

if __name__=="__main__":
    chc=CryptiHubCore()
    chc.start()