def process(self, diagnostic):
        """
        The default implementation of :meth:`process` renders non-fatal
        diagnostics to ``sys.stderr``, and raises fatal ones as a :class:`Error`.
        """
        diagnostic.notes += self._appended_notes
        self.render_diagnostic(diagnostic)
        if diagnostic.level == "fatal" or \
                (self.all_errors_are_fatal and diagnostic.level == "error"):
            raise Error(diagnostic)