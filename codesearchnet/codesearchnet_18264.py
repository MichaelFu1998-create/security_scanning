def sleep(self, channel):
        """Causes the bot to ignore all messages from the channel.

        Usage:
        !sleep [channel name] - ignore the specified channel (or current if none specified)
        """
        self.log.info('Sleeping in %s', channel)
        self._bot.dispatcher.ignore(channel)
        self.send_message(channel, 'Good night')