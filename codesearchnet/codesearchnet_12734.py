async def init_restart(self, error=None):
        """
            Restart the stream on error

        Parameters
        ----------
        error : bool, optional
            Whether to print the error or not
        """
        if error:
            utils.log_error(logger=logger)

        if self.state == DISCONNECTION:
            if self._error_timeout < MAX_DISCONNECTION_TIMEOUT:
                self._error_timeout += DISCONNECTION_TIMEOUT

            logger.info("The stream was disconnected, will reconnect in %ss"
                        % self._error_timeout)

        elif self.state == RECONNECTION:
            if self._error_timeout < RECONNECTION_TIMEOUT:
                self._error_timeout = RECONNECTION_TIMEOUT
            elif self._error_timeout < MAX_RECONNECTION_TIMEOUT:
                self._error_timeout *= 2

            logger.info("Could not connect to the stream, reconnection in %ss"
                        % self._error_timeout)

        elif self.state == ENHANCE_YOUR_CALM:
            if self._error_timeout < ENHANCE_YOUR_CALM_TIMEOUT:
                self._error_timeout = ENHANCE_YOUR_CALM_TIMEOUT
            else:
                self._error_timeout *= 2

            logger.warning("Enhance Your Calm response received from Twitter. "
                           "If you didn't restart your program frenetically "
                           "then there is probably something wrong with it. "
                           "Make sure you are not opening too many connections"
                           " to the endpoint you are currently using by "
                           "checking out Twitter's Streaming API "
                           "documentation: "
                           "https://dev.twitter.com/streaming/overview\n"
                           "The stream will restart in %ss."
                           % self._error_timeout)
        elif self.state == EOF:
            pass  # no timeout
        else:
            raise RuntimeError("Incorrect state: %d" % self.state)

        self._reconnecting = True
        return {'reconnecting_in': self._error_timeout, 'error': error}