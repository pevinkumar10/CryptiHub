

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