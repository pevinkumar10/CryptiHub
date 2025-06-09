class CryptiHubAuthenticator:
    """
        Class to used to authentication.

        Args:
            None

        Returns:
            None
    """
    def room_authenticator(self,current_room_id : str,user_sent_room_id: str) -> bool:
        """
            Function to authenticate the room.

            Args:
                current_room_id (str): The current room id.
                user_sent_room_id (str) : The user supplied room id.

            Returns:
                bool: True if both are same , False if not same.
        """
        if(current_room_id == user_sent_room_id):
            return True
        else:
            return False

                             