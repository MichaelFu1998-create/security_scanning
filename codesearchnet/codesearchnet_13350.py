def set_response_handlers(self, stanza, res_handler, err_handler,
                                    timeout_handler = None, timeout = None):
        """Set response handler for an IQ "get" or "set" stanza.

        This should be called before the stanza is sent.

        :Parameters:
            - `stanza`: an IQ stanza
            - `res_handler`: result handler for the stanza. Will be called
              when matching <iq type="result"/> is received. Its only
              argument will be the stanza received. The handler may return
              a stanza or list of stanzas which should be sent in response.
            - `err_handler`: error handler for the stanza. Will be called
              when matching <iq type="error"/> is received. Its only
              argument will be the stanza received. The handler may return
              a stanza or list of stanzas which should be sent in response
              but this feature should rather not be used (it is better not to
              respond to 'error' stanzas).
            - `timeout_handler`: timeout handler for the stanza. Will be called
              (with no arguments) when no matching <iq type="result"/> or <iq
              type="error"/> is received in next `timeout` seconds.
            - `timeout`: timeout value for the stanza. After that time if no
              matching <iq type="result"/> nor <iq type="error"/> stanza is
              received, then timeout_handler (if given) will be called.
        """
        # pylint: disable-msg=R0913
        self.lock.acquire()
        try:
            self._set_response_handlers(stanza, res_handler, err_handler,
                                                    timeout_handler, timeout)
        finally:
            self.lock.release()