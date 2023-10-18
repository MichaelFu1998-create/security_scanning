def context(self, *notes):
        """
        A context manager that appends ``note`` to every diagnostic processed by
        this engine.
        """
        self._appended_notes += notes
        yield
        del self._appended_notes[-len(notes):]