def locked_context(self, key=None, default=dict):
        """ Policy shared context dictionary """
        keys = ['policy']
        if key is not None:
            keys.append(key)
        with self._executor.locked_context('.'.join(keys), default) as policy_context:
            yield policy_context