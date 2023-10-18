def do_a(self, line):
        """Send the Master an AnalogInput (group 32) value. Command syntax is: a index value"""
        index, value_string = self.index_and_value_from_line(line)
        if index and value_string:
            try:
                self.application.apply_update(opendnp3.Analog(float(value_string)), index)
            except ValueError:
                print('Please enter a floating-point value as the second argument.')