def consume_line(self, line):
        """Consume data from a line."""
        data = RE_VALUE_KEY.split(line.strip(), 1)
        if len(data) == 1:
            return float(data[0]), None
        else:
            return float(data[0]), data[1].strip()