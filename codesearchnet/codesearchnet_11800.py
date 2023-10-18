def lenv(self):
        """
        Returns a version of env filtered to only include the variables in our namespace.
        """
        _env = type(env)()
        for _k, _v in six.iteritems(env):
            if _k.startswith(self.name+'_'):
                _env[_k[len(self.name)+1:]] = _v
        return _env