def connect(self):
        """Logs into the specified ftp server and returns connector."""
        for tried_connection_count in range(CFG_FTP_CONNECTION_ATTEMPTS):
            try:
                self.ftp = FtpHandler(self.config.OXFORD.URL,
                                      self.config.OXFORD.LOGIN,
                                      self.config.OXFORD.PASSWORD)
                self.logger.debug(("Successful connection to the "
                                   "Oxford University Press server"))
                return
            except socket_timeout_exception as err:
                self.logger.error(('Failed to connect %d of %d times. '
                                   'Will sleep for %d seconds and try again.')
                                  % (tried_connection_count+1,
                                     CFG_FTP_CONNECTION_ATTEMPTS,
                                     CFG_FTP_TIMEOUT_SLEEP_DURATION))
                time.sleep(CFG_FTP_TIMEOUT_SLEEP_DURATION)
            except Exception as err:
                self.logger.error(('Failed to connect to the Oxford '
                                   'University Press server. %s') % (err,))
                break

        raise LoginException(err)