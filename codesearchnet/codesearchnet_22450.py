def squeeze_words(line, width=60):
        """ Remove spaces in between words until it is small enough for
            `width`.
            This will always leave at least one space between words,
            so it may not be able to get below `width` characters.
        """
        # Start removing spaces to "squeeze" the text, leaving at least one.
        while ('  ' in line) and (len(line) > width):
            # Remove two spaces from the end, replace with one.
            head, _, tail = line.rpartition('  ')
            line = ' '.join((head, tail))
        return line