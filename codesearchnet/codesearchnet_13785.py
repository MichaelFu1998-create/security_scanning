def parse_module(self):
        """Parse a module (and its children) and return a Module object."""
        self.log.debug("parsing module.")
        start = self.line
        docstring = self.parse_docstring()
        children = list(self.parse_definitions(Module, all=True))
        assert self.current is None, self.current
        end = self.line
        cls = Module
        if self.filename.endswith("__init__.py"):
            cls = Package
        module = cls(
            self.filename,
            self.source,
            start,
            end,
            [],
            docstring,
            children,
            None,
            self.all,
            None,
            "",
        )
        for child in module.children:
            child.parent = module
        module.future_imports = self.future_imports
        self.log.debug("finished parsing module.")
        return module