def unset_logging(self):
        """ Mute newly added handlers to the root level, right after calling executor.status
        """
        if self.logger_flag is True:
            return

        root_logger = logging.getLogger()

        for hndlr in root_logger.handlers:
            if hndlr not in self.prior_loghandlers:
                hndlr.setLevel(logging.ERROR)

        self.logger_flag = True