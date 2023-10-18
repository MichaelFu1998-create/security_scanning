def getLogLevel(self, section, option):
          """Return the textual representation of logging level 'option' or the number.

          Note that option is always interpreted as an UPPERCASE string
          and hence integer log levels will not be recognized.

          .. SeeAlso: :mod:`logging` and :func:`logging.getLevelName`
          """
          return logging.getLevelName(self.get(section, option).upper())