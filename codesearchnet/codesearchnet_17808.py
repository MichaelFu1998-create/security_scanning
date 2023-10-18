def get_poll(self, arg, *, request_policy=None):
        """Retrieves a poll from strawpoll.

        :param arg: Either the ID of the poll or its strawpoll url.
        :param request_policy: Overrides :attr:`API.requests_policy` for that \
        request.
        :type request_policy: Optional[:class:`RequestsPolicy`]

        :raises HTTPException: Requesting the poll failed.

        :returns: A poll constructed with the requested data.
        :rtype: :class:`Poll`
        """
        if isinstance(arg, str):
            # Maybe we received an url to parse
            match = self._url_re.match(arg)
            if match:
                arg = match.group('id')

        return self._http_client.get('{}/{}'.format(self._POLLS, arg),
                                     request_policy=request_policy,
                                     cls=strawpoll.Poll)