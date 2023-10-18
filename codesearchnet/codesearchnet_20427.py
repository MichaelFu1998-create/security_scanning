def reverse(self):
        """ Reverse all bumpers """
        if not self.test_drive and self.bumps:
            map(lambda b: b.reverse(), self.bumpers)