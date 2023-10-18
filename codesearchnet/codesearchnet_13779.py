def parse(self, filelike, filename):
        """Parse the given file-like object and return its Module object."""
        self.log = log
        self.source = filelike.readlines()
        src = "".join(self.source)
        # This may raise a SyntaxError:
        compile(src, filename, "exec")
        self.stream = TokenStream(StringIO(src))
        self.filename = filename
        self.all = None
        self.future_imports = set()
        self._accumulated_decorators = []
        return self.parse_module()