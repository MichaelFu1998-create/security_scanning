def check_file(self, filename):
        # type: (str) -> bool
        """
        Overrides :py:meth:`.Config.check_file`
        """
        can_read = super(SecuredConfig, self).check_file(filename)
        if not can_read:
            return False

        mode = get_stat(filename).st_mode
        if (mode & stat.S_IRGRP) or (mode & stat.S_IROTH):
            msg = "File %r is not secure enough. Change it's mode to 600"
            self._log.warning(msg, filename)
            return False
        return True