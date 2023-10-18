def send_message(self, channel, text):
        """
        Used to send a message to the specified channel.

        * channel - can be a channel or user
        * text - message to send
        """
        if isinstance(channel, SlackIM) or isinstance(channel, SlackUser):
            self._bot.send_im(channel, text)
        elif isinstance(channel, SlackRoom):
            self._bot.send_message(channel, text)
        elif isinstance(channel, basestring):
            if channel[0] == '@':
                self._bot.send_im(channel[1:], text)
            elif channel[0] == '#':
                self._bot.send_message(channel[1:], text)
            else:
                self._bot.send_message(channel, text)
        else:
            self._bot.send_message(channel, text)