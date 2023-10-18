def index_from_line(line):
        """Parse an index (integer) from command line args and return it."""
        try:
            index = int(line.split(' ')[0])
        except (ValueError, IndexError):
            print('Please enter an integer index as the first argument.')
            index = None
        return index