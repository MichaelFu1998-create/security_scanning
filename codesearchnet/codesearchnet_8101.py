def update(self, desc=None, **kwds):
        """This method updates the description much like dict.update(), *except*:

        1. for description which have dictionary values, it uses update
           to alter the existing value and does not replace them.

        2. `None` is a special value that means "clear section to default" or
           "delete field".
        """
        sections.update(self._desc, desc, **kwds)