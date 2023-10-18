def _check_next(self):
    """Checks if a next message is possible.

    :returns: True if a next message is possible, otherwise False
    :rtype: bool

    """
    if self.is_initial:
      return True
    if self.before:
      if self.before_cursor:
        return True
      else:
        return False
    else:
      if self.after_cursor:
        return True
      else:
        return False