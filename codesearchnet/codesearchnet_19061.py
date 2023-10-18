def set_script(self, i):
        """
        set the value of delta to reflect the current codepage
        
        """

        if i in range(1, 10):
            n = i - 1
        else:
            raise IllegalInput("Invalid Value for ATR %s" % (hex(i)))

        if n > -1: # n = -1 is the default script ..
            self.curr_script = n
            self.delta = n * DELTA
        
        return