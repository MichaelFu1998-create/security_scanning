async def _get_socket_url(self):
        """Get the WebSocket URL for the RTM session.

        Warning:
          The URL expires if the session is not joined within 30
          seconds of the API call to the start endpoint.

        Returns:
          :py:class:`str`: The socket URL.

        """
        data = await self.api.execute_method(
            self.RTM_START_ENDPOINT,
            simple_latest=True,
            no_unreads=True,
        )
        return data['url']