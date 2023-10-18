def _exec(self, globals_dict=None):
        """exec compiled code"""
        globals_dict = globals_dict or {}
        globals_dict.setdefault('__builtins__', {})
        exec(self._code, globals_dict)
        return globals_dict