def log(self, level, msg, *args, **kwargs):
      """
      Log 'msg % args' with the integer severity 'level'.

      To pass exception information, use the keyword argument exc_info with
      a true value, e.g.

      logger.log(level, "We have a %s", "mysterious problem", exc_info=1)
      """
      self._baseLogger.log(self, level, self.getExtendedMsg(msg), *args,
                           **kwargs)