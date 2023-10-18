def do_d(self, line):
        """Send the Master a DoubleBitBinaryInput (group 4) value of DETERMINED_ON. Command syntax is: d index"""
        index = self.index_from_line(line)
        if index:
            self.application.apply_update(opendnp3.DoubleBitBinary(opendnp3.DoubleBit.DETERMINED_ON), index)