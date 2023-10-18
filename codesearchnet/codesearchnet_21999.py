def line(self, line):
        """Returns list of strings split by input delimeter

        Argument:
        line - Input line to cut
        """
        # Remove empty strings in case of multiple instances of delimiter
        return [x for x in re.split(self.delimiter, line.rstrip()) if x != '']