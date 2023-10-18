def challenge(self, challenge):
        """Process a challenge and return the response.

        :Parameters:
            - `challenge`: the challenge from server.
        :Types:
            - `challenge`: `bytes`

        :return: the response or a failure indicator.
        :returntype: `sasl.Response` or `sasl.Failure`
        """
        # pylint: disable=R0911
        if not challenge:
            logger.debug("Empty challenge")
            return Failure("bad-challenge")

        if self._server_first_message:
            return self._final_challenge(challenge)

        match = SERVER_FIRST_MESSAGE_RE.match(challenge)
        if not match:
            logger.debug("Bad challenge syntax: {0!r}".format(challenge))
            return Failure("bad-challenge")

        self._server_first_message = challenge

        mext = match.group("mext")
        if mext:
            logger.debug("Unsupported extension received: {0!r}".format(mext))
            return Failure("bad-challenge")

        nonce = match.group("nonce")
        if not nonce.startswith(self._c_nonce):
            logger.debug("Nonce does not start with our nonce")
            return Failure("bad-challenge")

        salt = match.group("salt")
        try:
            salt = a2b_base64(salt)
        except ValueError:
            logger.debug("Bad base64 encoding for salt: {0!r}".format(salt))
            return Failure("bad-challenge")

        iteration_count = match.group("iteration_count")
        try:
            iteration_count = int(iteration_count)
        except ValueError:
            logger.debug("Bad iteration_count: {0!r}".format(iteration_count))
            return Failure("bad-challenge")

        return self._make_response(nonce, salt, iteration_count)