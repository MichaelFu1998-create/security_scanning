def repeat(self, n=2, oscillate=False, callback=None):
        """
        Returns a list that is a repetition of the given list.

        When oscillate is True,
        moves from the end back to the beginning,
        and then from the beginning to the end, and so on.
        """
        colorlist = ColorList()
        colors = ColorList.copy(self)
        for i in _range(n):
            colorlist.extend(colors)
            if oscillate: colors = colors.reverse()
            if callback: colors = callback(colors)

        return colorlist