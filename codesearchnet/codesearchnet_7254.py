async def _fetch_channel_sid(self):
        """Creates a new channel for receiving push data.

        Sending an empty forward channel request will create a new channel on
        the server.

        There's a separate API to get the gsessionid alone that Hangouts for
        Chrome uses, but if we don't send a gsessionid with this request, it
        will return a gsessionid as well as the SID.

        Raises hangups.NetworkError if the channel can not be created.
        """
        logger.info('Requesting new gsessionid and SID...')
        # Set SID and gsessionid to None so they aren't sent in by send_maps.
        self._sid_param = None
        self._gsessionid_param = None
        res = await self.send_maps([])
        self._sid_param, self._gsessionid_param = _parse_sid_response(res.body)
        logger.info('New SID: {}'.format(self._sid_param))
        logger.info('New gsessionid: {}'.format(self._gsessionid_param))