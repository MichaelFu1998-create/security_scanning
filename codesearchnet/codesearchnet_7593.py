def frequencies(self, sides=None):

        """Return the frequency vector according to :attr:`sides`"""
        # use the attribute sides except if a valid sides argument is provided
        if sides is None:
            sides = self.sides
        if sides not in self._sides_choices:
            raise errors.SpectrumChoiceError(sides, self._sides_choices)

        if sides == 'onesided':
            return self._range.onesided()
        if sides == 'twosided':
            return self._range.twosided()
        if sides == 'centerdc':
            return self._range.centerdc()