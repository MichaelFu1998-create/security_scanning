def set_level(self, level='info', handlers=None):
        """
        Set the logging level (which types of logs are actually printed / recorded)
        to one of ['debug', 'info', 'warn', 'error', 'fatal'] in that order
        of severity
        """
        for h in self.get_handlers(handlers):
            h.setLevel(levels[level])