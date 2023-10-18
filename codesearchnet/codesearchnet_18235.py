def send_im(self, user, text):
        """
        Sends a message to a user as an IM

        * user - The user to send to.  This can be a SlackUser object, a user id, or the username (without the @)
        * text - String to send
        """
        if isinstance(user, SlackUser):
            user = user.id
            channelid = self._find_im_channel(user)
        else:
            channelid = user.id
        self.send_message(channelid, text)