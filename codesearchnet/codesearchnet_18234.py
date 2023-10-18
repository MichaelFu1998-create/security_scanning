def send_message(self, channel, text, thread=None, reply_broadcast=None):
        """
        Sends a message to the specified channel

        * channel - The channel to send to.  This can be a SlackChannel object, a channel id, or a channel name
        (without the #)
        * text - String to send
        * thread - reply to the thread. See https://api.slack.com/docs/message-threading#threads_party
        * reply_broadcast - Set to true to indicate your reply is germane to all members of a channel
        """
        # This doesn't want the # in the channel name
        if isinstance(channel, SlackRoomIMBase):
            channel = channel.id
        self.log.debug("Trying to send to %s: %s", channel, text)
        self.sc.rtm_send_message(channel, text, thread=thread, reply_broadcast=reply_broadcast)