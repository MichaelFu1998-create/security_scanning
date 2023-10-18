def is_annotation(self, i=0):
        """ Returns true if the position is the start of an annotation application
        (as opposed to an annotation declaration)

        """

        return (isinstance(self.tokens.look(i), Annotation)
                and not self.tokens.look(i + 1).value == 'interface')