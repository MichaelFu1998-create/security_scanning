def communicate(self, use_input=True):
        """Run the command, using the input that was set up on __init__ (for *use_input* = ``True``)"""
        if use_input:
            return super(PopenWithInput, self).communicate(self.input)
        else:
            return super(PopenWithInput, self).communicate()