def error(self, fail=True, action=''):
        """
        SHOULD BE PRIVATE METHOD
        """
        e = 'There was an unknown error communicating with the device.'
        if action:
            e = 'While %s: %s' % (action, e)
        log.error(e)
        if fail:
            raise IOError(e)