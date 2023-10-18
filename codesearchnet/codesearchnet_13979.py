def reload_functions(self):
        """
        Replace functions in namespace with functions from edited_source.
        """
        with LiveExecution.lock:
            if self.edited_source:
                tree = ast.parse(self.edited_source)
                for f in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]:
                    self.ns[f.name].__code__ = meta.decompiler.compile_func(f, self.filename, self.ns).__code__