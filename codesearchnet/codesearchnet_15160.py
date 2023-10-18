def _walk(self):
        """Loop through all the instructions that are `_todo`."""
        while self._todo:
            args = self._todo.pop(0)
            self._step(*args)