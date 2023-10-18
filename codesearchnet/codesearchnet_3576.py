def _top(self, n=0):
        """Read a value from the top of the stack without removing it"""
        if len(self.stack) - n < 0:
            raise StackUnderflow()
        return self.stack[n - 1]