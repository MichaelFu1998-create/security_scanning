def get_spec(self):
        """
        Parse this process (if it has not already been parsed), and return the
        workflow spec.
        """
        if self.is_parsed:
            return self.spec
        if self.parsing_started:
            raise NotImplementedError(
                'Recursive call Activities are not supported.')
        self._parse()
        return self.get_spec()