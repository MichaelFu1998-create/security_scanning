def parse(self, source):
        """Parse command content from the LaTeX source.

        Parameters
        ----------
        source : `str`
            The full source of the tex document.

        Yields
        ------
        parsed_command : `ParsedCommand`
            Yields parsed commands instances for each occurence of the command
            in the source.
        """
        command_regex = self._make_command_regex(self.name)
        for match in re.finditer(command_regex, source):
            self._logger.debug(match)
            start_index = match.start(0)
            yield self._parse_command(source, start_index)