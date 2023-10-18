def _parse_command(self, source, start_index):
        """Parse a single command.

        Parameters
        ----------
        source : `str`
            The full source of the tex document.
        start_index : `int`
            Character index in ``source`` where the command begins.

        Returns
        -------
        parsed_command : `ParsedCommand`
            The parsed command from the source at the given index.
        """
        parsed_elements = []

        # Index of the parser in the source
        running_index = start_index

        for element in self.elements:
            opening_bracket = element['bracket']
            closing_bracket = self._brackets[opening_bracket]

            # Find the opening bracket.
            element_start = None
            element_end = None
            for i, c in enumerate(source[running_index:], start=running_index):
                if c == element['bracket']:
                    element_start = i
                    break
                elif c == '\n':
                    # No starting bracket on the line.
                    if element['required'] is True:
                        # Try to parse a single single-word token after the
                        # command, like '\input file'
                        content = self._parse_whitespace_argument(
                            source[running_index:],
                            self.name)
                        return ParsedCommand(
                            self.name,
                            [{'index': element['index'],
                              'name': element['name'],
                              'content': content.strip()}],
                            start_index,
                            source[start_index:i])
                    else:
                        # Give up on finding an optional element
                        break

            # Handle cases when the opening bracket is never found.
            if element_start is None and element['required'] is False:
                # Optional element not found. Continue to next element,
                # not advancing the running_index of the parser.
                continue
            elif element_start is None and element['required'] is True:
                message = ('Parsing command {0} at index {1:d}, '
                           'did not detect element {2:d}'.format(
                               self.name,
                               start_index,
                               element['index']))
                raise CommandParserError(message)

            # Find the closing bracket, keeping track of the number of times
            # the same type of bracket was opened and closed.
            balance = 1
            for i, c in enumerate(source[element_start + 1:],
                                  start=element_start + 1):
                if c == opening_bracket:
                    balance += 1
                elif c == closing_bracket:
                    balance -= 1

                if balance == 0:
                    element_end = i
                    break

            if balance > 0:
                message = ('Parsing command {0} at index {1:d}, '
                           'did not find closing bracket for required '
                           'command element {2:d}'.format(
                               self.name,
                               start_index,
                               element['index']))
                raise CommandParserError(message)

            # Package the parsed element's content.
            element_content = source[element_start + 1:element_end]
            parsed_element = {
                'index': element['index'],
                'name': element['name'],
                'content': element_content.strip()
            }
            parsed_elements.append(parsed_element)

            running_index = element_end + 1

        command_source = source[start_index:running_index]
        parsed_command = ParsedCommand(self.name, parsed_elements,
                                       start_index, command_source)
        return parsed_command