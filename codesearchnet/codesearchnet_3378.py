def context(self):
        """ Convenient access to shared context """
        if self._context is not None:
            return self._context
        else:
            logger.warning("Using shared context without a lock")
            return self._executor._shared_context