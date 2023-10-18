def _format_message(self, channel, text):
        """Format an outgoing message for transmission.

        Note:
          Adds the message type (``'message'``) and incremental ID.

        Arguments:
          channel (:py:class:`str`): The channel to send to.
          text (:py:class:`str`): The message text to send.

        Returns:
          :py:class:`str`: The JSON string of the message.

        """
        payload = {'type': 'message', 'id': next(self._msg_ids)}
        payload.update(channel=channel, text=text)
        return json.dumps(payload)