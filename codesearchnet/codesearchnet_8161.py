def apply(self, function):
        """
        For each row or column in cuts, read a list of its colors,
        apply the function to that list of colors, then write it back
        to the layout.
        """
        for cut in self.cuts:
            value = self.read(cut)
            function(value)
            self.write(cut, value)