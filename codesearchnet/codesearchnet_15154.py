def _expand(self, row, consumed_position, passed):
        """Add the arguments `(args, kw)` to `_walk` to the todo list."""
        self._todo.append((row, consumed_position, passed))