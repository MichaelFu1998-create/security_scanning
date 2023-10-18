def log(self, message, level=logging.DEBUG):
        """
        Logs the message in the root logger with the log level
        @param message: Message to be logged
        @type message: string
        @param level: Log level, defaul DEBUG
        @type level: integer
    
        @return: 1 on success and 0 on error
        @rtype: integer
        """
        if _ldtp_debug:
            print(message)
        self.logger.log(level, str(message))
        return 1