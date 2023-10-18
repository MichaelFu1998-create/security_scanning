def __comment(self):
        """Level-1 parser for comments.

        pattern: #.*
        Append comment (with initial '# ' stripped) to all comments.
        """
        tok = self.__consume()
        self.DXfield.add_comment(tok.value())
        self.set_parser('general')