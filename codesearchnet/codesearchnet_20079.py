async def join_rtm(self, filters=None):
        """Join the real-time messaging service.

        Arguments:
          filters (:py:class:`dict`, optional): Dictionary mapping
            message filters to the functions they should dispatch to.
            Use a :py:class:`collections.OrderedDict` if precedence is
            important; only one filter, the first match, will be
            applied to each message.

        """
        if filters is None:
            filters = [cls(self) for cls in self.MESSAGE_FILTERS]
        url = await self._get_socket_url()
        logger.debug('Connecting to %r', url)
        async with ws_connect(url) as socket:
            first_msg = await socket.receive()
            self._validate_first_message(first_msg)
            self.socket = socket
            async for message in socket:
                if message.tp == MsgType.text:
                    await self.handle_message(message, filters)
                elif message.tp in (MsgType.closed, MsgType.error):
                    if not socket.closed:
                        await socket.close()
                    self.socket = None
                    break
        logger.info('Left real-time messaging.')