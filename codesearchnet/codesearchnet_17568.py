def _prepare_lines(self, lines):
        """
        Prepare the lines read from the text file before starting to process
        it.
        """

        result = list()
        for line in lines:
            # Remove all whitespace characters (e.g. spaces, line breaks, etc.)
            # from the start and end of the line.
            line = line.strip()
            # Replace all tabs with spaces.
            line = line.replace("\t", " ")
            # Replace all repeating spaces with a single space.
            while line.find("  ") > -1:
                line = line.replace("  ", " ")
            result.append(line)
        return result