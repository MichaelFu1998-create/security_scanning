def stoplog(self):
        """ Stop logging.
    
        @return: 1 on success and 0 on error
        @rtype: integer
        """
        if self._file_logger:
            self.logger.removeHandler(_file_logger)
            self._file_logger = None
        return 1