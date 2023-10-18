def _extendrange(self, start, end):
        """Creates list of values in a range with output delimiters.

        Arguments:
            start -     range start
            end -       range end
        """
        range_positions = []
        for i in range(start, end):
            if i != 0:
                range_positions.append(str(i))
            if i < end:
                range_positions.append(self.separator)
        return range_positions