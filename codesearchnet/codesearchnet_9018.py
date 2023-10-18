def do_b0(self, line):
        """Send the Master a BinaryInput (group 2) value of False at index 6. Command syntax is: b0"""
        self.application.apply_update(opendnp3.Binary(False), index=6)