def code(self, code):
        """ Decorator to associate a code to an exception """
        def decorator(exception):
            self[code] = exception
            return exception

        return decorator