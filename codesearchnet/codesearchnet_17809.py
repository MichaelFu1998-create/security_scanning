def submit_poll(self, poll, *, request_policy=None):
        """Submits a poll on strawpoll.

        :param poll: The poll to submit.
        :type poll: :class:`Poll`
        :param request_policy: Overrides :attr:`API.requests_policy` for that \
        request.
        :type request_policy: Optional[:class:`RequestsPolicy`]

        :raises ExistingPoll: This poll instance has already been submitted.
        :raises HTTPException: The submission failed.

        :returns: The given poll updated with the data sent back from the submission.
        :rtype: :class:`Poll`

        .. note::
            Only polls that have a non empty title and between 2 and 30 options
            can be submitted.
        """
        if poll.id is not None:
            raise ExistingPoll()

        options = poll.options
        data = {
            'title': poll.title,
            'options': options,
            'multi': poll.multi,
            'dupcheck': poll.dupcheck,
            'captcha': poll.captcha
        }

        return self._http_client.post(self._POLLS,
                                      data=data,
                                      request_policy=request_policy,
                                      cls=strawpoll.Poll)