def format(self, record):
        """tweaked from source of base"""
        try:
            record.message = record.getMessage()
        except TypeError:
            # if error during msg = msg % self.args
            if record.args:
                if isinstance(record.args, collections.Mapping):
                    record.message = record.msg.format(**record.args)
                else:
                    record.message = record.msg.format(record.args)
        self._fmt = self.getfmt(record.levelname)
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        s = self._fmt.format(**record.__dict__)

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != '\n':
                s += '\n'
            try:
                s = s + record.exc_text
            except UnicodeError:
                s = s + record.exc_text.decode(sys.getfilesystemencoding(), 'replace')
        return s