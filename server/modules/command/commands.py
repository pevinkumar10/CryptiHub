
try:
    from modules import connected_host_lock , connected_users
except ImportError as Ie:
    print(f"Error [modules.command]:{Ie} ")

class ServerCommands():
    def help(self):
        return """
    ###########################################################################
    ###########################################################################
    ####                                                                   ####
    ###                    --== CrypiHub Commands =--                       ###
    ####                                                                   ####
    ###     /help                   - To see available commands.            ###
    ####                                                                   ####
    ###     /users                  - To see all the users in the chat.     ###
    ####                                                                   ####
    ###     /ban                    - To ban a user.                        ###
    ####                                                                   ####
    ###     /unban                  - To unban a user.                      ###
    ####                                                                   ####
    ###     /kick                   - To remove a user from chat.           ###
    ####                                                                   ####
    ###                                                                     ###
    ###########################################################################
    ###########################################################################
"""

    def get_all_users(self,users):
        return users.keys()
    
    # def info_broadcaster(self,username,state):
    #     with connected_host_lock:
    #         for value in connected_users.values():
    #             address=value['address']
    #             conn=value['conn']
    #             try:
    #                 send_message=f"\tserver: {username} is {state} from the chat"
    #                 conn.sendall(send_message.encode())
    #                 conn.sendall("exit".encode())
                    
    #             except Exception as E:
    #                 print(f"couldn't proadcast message 2: {E}")

    #             finally:
    #                 conn.close()

    # def kickout_user(self,username):
    #     with connected_host_lock:
    #         if username in connected_users:
    #             del connected_users[username]
    #     self.info_broadcaster(username,"kicked")
