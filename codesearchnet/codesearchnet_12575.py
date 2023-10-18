def use(cls, name, method: [str, Set, List], url=None):
        """ interface helper function"""
        if not isinstance(method, (str, list, set, tuple)):
            raise BaseException('Invalid type of method: %s' % type(method).__name__)

        if isinstance(method, str):
            method = {method}

        # TODO: check methods available
        cls._interface[name] = [{'method': method, 'url': url}]