def _get_function_ptr(self, name):
        """Get or create a function pointer of the given name."""
        func = _make_function_ptr_instance
        self._function_ptrs.setdefault(name, func(self, name))
        return self._function_ptrs[name]