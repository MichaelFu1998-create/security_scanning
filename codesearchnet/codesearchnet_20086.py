def _respond(self, channel, text):
        """Respond to a message on the current socket.

        Args:
          channel (:py:class:`str`): The channel to send to.
          text (:py:class:`str`): The message text to send.

        """
        result = self._format_message(channel, text)
        if result is not None:
            logger.info(
                'Sending message: %r',
                truncate(result, max_len=50),
            )
        self.socket.send_str(result)