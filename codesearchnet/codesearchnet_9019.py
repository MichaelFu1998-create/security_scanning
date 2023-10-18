def do_c(self, line):
        """Send the Master a Counter (group 22) value. Command syntax is: c index value"""
        index, value_string = self.index_and_value_from_line(line)
        if index and value_string:
            try:
                self.application.apply_update(opendnp3.Counter(int(value_string)), index)
            except ValueError:
                print('Please enter an integer value as the second argument.')