def get_personalities(self, line):
        """Return a list of personalities readed from the input line."""
        return [split('\W+', i)[1] for i in line.split(':')[1].split(' ') if i.startswith('[')]