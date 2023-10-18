def input(self, file):
        """
        Load lexer with content from `file` which can be a path or a file
        like object.
        """
        if isinstance(file, string_types):
            with open(file) as f:
                self.lexer.input(f.read())
        else:
            self.lexer.input(file.read())