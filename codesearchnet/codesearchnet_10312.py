def parse_selection(self, selection, name=None):
        """Retuns (groupname, filename) with index group."""

        if type(selection) is tuple:
            # range
            process = self._process_range
        elif selection.startswith('@'):
            # verbatim make_ndx command
            process = self._process_command
            selection = selection[1:]
        else:
            process = self._process_residue
        return process(selection, name)