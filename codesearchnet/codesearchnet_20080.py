async def handle_message(self, message, filters):
        """Handle an incoming message appropriately.

        Arguments:
          message (:py:class:`aiohttp.websocket.Message`): The incoming
            message to handle.
          filters (:py:class:`list`): The filters to apply to incoming
            messages.

        """
        data = self._unpack_message(message)
        logger.debug(data)
        if data.get('type') == 'error':
            raise SlackApiError(
                data.get('error', {}).get('msg', str(data))
            )
        elif self.message_is_to_me(data):
            text = data['text'][len(self.address_as):].strip()
            if text == 'help':
                return self._respond(
                    channel=data['channel'],
                    text=self._instruction_list(filters),
                )
            elif text == 'version':
                return self._respond(
                    channel=data['channel'],
                    text=self.VERSION,
                )
        for _filter in filters:
            if _filter.matches(data):
                logger.debug('Response triggered')
                async for response in _filter:
                    self._respond(channel=data['channel'], text=response)