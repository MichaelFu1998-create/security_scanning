def wake(self, channel):
        """Causes the bot to resume operation in the channel.

        Usage:
        !wake [channel name] - unignore the specified channel (or current if none specified)
        """
        self.log.info('Waking up in %s', channel)
        self._bot.dispatcher.unignore(channel)
        self.send_message(channel, 'Hello, how may I be of service?')