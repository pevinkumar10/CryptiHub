class CryptiHubAuthenticator():
    def room_authenticator(self,current_room_id,user_sent_room_id):
        if(current_room_id == user_sent_room_id):
            return True
        else:
            return False

                             