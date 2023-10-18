def index_and_value_from_line(line):
        """Parse an index (integer) and value (string) from command line args and return them."""
        try:
            index = int(line.split(' ')[0])
        except (ValueError, IndexError):
            print('Please enter an integer index as the first argument.')
            index = None
        try:
            value_string = line.split(' ')[1]
        except (ValueError, IndexError):
            print('Please enter a second argument.')
            value_string = None
        return index, value_string