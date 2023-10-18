def poll(self, url, initial_delay=2, delay=1, tries=20, errors=STRICT, is_complete_callback=None, **params):
        """
        Poll the URL
        :param url - URL to poll, should be returned by 'create_session' call
        :param initial_delay - specifies how many seconds to wait before the first poll
        :param delay - specifies how many seconds to wait between the polls
        :param tries - number of polls to perform
        :param errors - errors handling mode, see corresponding parameter in 'make_request' method
        :param params - additional query params for each poll request
        """
        time.sleep(initial_delay)
        poll_response = None

        if is_complete_callback == None:
            is_complete_callback = self._default_poll_callback

        for n in range(tries):
            poll_response = self.make_request(url, headers=self._headers(),
                                              errors=errors, **params)

            if is_complete_callback(poll_response):
                return poll_response
            else:
                time.sleep(delay)

        if STRICT == errors:
            raise ExceededRetries(
                "Failed to poll within {0} tries.".format(tries))
        else:
            return poll_response