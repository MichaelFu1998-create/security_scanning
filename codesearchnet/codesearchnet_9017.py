def do_b(self, line):
        """Send the Master a BinaryInput (group 2) value. Command syntax is: 'b index true' or 'b index false'"""
        index, value_string = self.index_and_value_from_line(line)
        if index and value_string:
            if value_string.lower() == 'true' or value_string.lower() == 'false':
                self.application.apply_update(opendnp3.Binary(value_string == 'true'), index)
            else:
                print('Please enter true or false as the second argument.')