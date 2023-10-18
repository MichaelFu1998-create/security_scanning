def set_formatter(self, formatter='standard', handlers=None):
        """
        Set the text format of messages to one of the pre-determined forms,
        one of ['quiet', 'minimal', 'standard', 'verbose']
        """
        for h in self.get_handlers(handlers):
            h.setFormatter(logging.Formatter(formatters[formatter]))