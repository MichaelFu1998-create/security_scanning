def warning(self, msg, *args, **kwargs):
    """
    Log 'msg % args' with severity 'WARNING'.

    To pass exception information, use the keyword argument exc_info with
    a true value, e.g.

    logger.warning("Houston, we have a %s", "bit of a problem", exc_info=1)
    """
    self._baseLogger.warning(self, self.getExtendedMsg(msg), *args, **kwargs)