def finish(self, data):
        """Process success indicator from the server.

        Process any addiitional data passed with the success.
        Fail if the server was not authenticated.

        :Parameters:
            - `data`: an optional additional data with success.
        :Types:
            - `data`: `bytes`

        :return: success or failure indicator.
        :returntype: `sasl.Success` or `sasl.Failure`"""
        if not self._server_first_message:
            logger.debug("Got success too early")
            return Failure("bad-success")
        if self._finished:
            return Success({"username": self.username, "authzid": self.authzid})
        else:
            ret = self._final_challenge(data)
            if isinstance(ret, Failure):
                return ret
            if self._finished:
                return Success({"username": self.username,
                                                    "authzid": self.authzid})
            else:
                logger.debug("Something went wrong when processing additional"
                                                        " data with success?")
                return Failure("bad-success")