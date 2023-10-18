def _remove_trailing_spaces(line):
        """Remove trailing spaces unless they are quoted with a backslash."""
        while line.endswith(' ') and not line.endswith('\\ '):
            line = line[:-1]
        return line.replace('\\ ', ' ')