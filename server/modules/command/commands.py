
try:
    from modules import connected_host_lock , connected_users
except ImportError as Ie:
    print(f"Error [modules.command]:{Ie} ")

class ServerCommands:
    """
        Class to handle the server commands.
    """
    def help(self) -> str:
        """
            Function to get the help menu for the CryptiHub.

            Args:
                None

            Returns:
                str: Returns help menu for the CryptiHub
        """
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
    ###     /stop                   - To stop the server.                   ###
    ####                                                                   ####
    ###                                                                     ###
    ###########################################################################
    ###########################################################################
"""

    def get_all_users(self,users : dict) -> list:
        """
            Function to get all the users in the chat.

            Args:
                Users in dict

            Returns:
                List: Username of all users in the chat as list.
        """
        return users.keys()
