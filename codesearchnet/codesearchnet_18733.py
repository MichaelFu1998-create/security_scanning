def body(self):
        """get the contents of the script"""
        if not hasattr(self, '_body'):
            self._body = inspect.getsource(self.module)
        return self._body