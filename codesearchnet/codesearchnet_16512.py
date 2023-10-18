def value(self,ascode=None):
        """Return text cast to the correct type or the selected type"""
        if ascode is None:
            ascode = self.code
        return self.cast[ascode](self.text)