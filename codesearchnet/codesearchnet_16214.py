def check_unused_args(self, used_args, args, kwargs):
        """Implement the check_unused_args in superclass."""
        for k, v in kwargs.items():
            if k in used_args:
                self._used_kwargs.update({k: v})
            else:
                self._unused_kwargs.update({k: v})