def method_exists(cls, method):
        """Whether a given method exists in the known API.

        Arguments:
          method (:py:class:`str`): The name of the method.

        Returns:
          :py:class:`bool`: Whether the method is in the known API.

        """
        methods = cls.API_METHODS
        for key in method.split('.'):
            methods = methods.get(key)
            if methods is None:
                break
        if isinstance(methods, str):
            logger.debug('%r: %r', method, methods)
            return True
        return False