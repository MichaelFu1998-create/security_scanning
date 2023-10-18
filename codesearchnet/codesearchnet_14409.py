def set(self, name, value):
        """ Changes a setting value.

            This implements a locking mechanism to ensure some level of thread
            safety.

            :param str name: Setting key name.
            :param value: Setting value.

        """
        if not self.settings.get('pyconfig.case_sensitive', False):
            name = name.lower()
        log.info("    %s = %s", name, repr(value))

        # Acquire our lock to change the config
        with self.mut_lock:
            self.settings[name] = value