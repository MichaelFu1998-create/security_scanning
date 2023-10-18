def format(self, record):
        """Customize the message format based on the log level."""
        if isinstance(self.fmt, dict):
            self._fmt = self.fmt[record.levelname]
            if sys.version_info > (3, 2):
                # Update self._style because we've changed self._fmt
                # (code based on stdlib's logging.Formatter.__init__())
                if self.style not in logging._STYLES:
                    raise ValueError('Style must be one of: %s' % ','.join(
                        list(logging._STYLES.keys())))
                self._style = logging._STYLES[self.style][0](self._fmt)

        if sys.version_info > (2, 7):
            message = super(LevelFormatter, self).format(record)
        else:
            message = ColoredFormatter.format(self, record)

        return message