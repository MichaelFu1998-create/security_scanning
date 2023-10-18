def _validate_first_message(cls, msg):
        """Check the first message matches the expected handshake.

        Note:
          The handshake is provided as :py:attr:`RTM_HANDSHAKE`.

        Arguments:
          msg (:py:class:`aiohttp.Message`): The message to validate.

        Raises:
          :py:class:`SlackApiError`: If the data doesn't match the
            expected handshake.

        """
        data = cls._unpack_message(msg)
        logger.debug(data)
        if data != cls.RTM_HANDSHAKE:
            raise SlackApiError('Unexpected response: {!r}'.format(data))
        logger.info('Joined real-time messaging.')