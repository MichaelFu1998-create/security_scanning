def reboot_or_dryrun(self, *args, **kwargs):
        """
        Reboots the server and waits for it to come back.
        """
        warnings.warn('Use self.run() instead.', DeprecationWarning, stacklevel=2)
        self.reboot(*args, **kwargs)