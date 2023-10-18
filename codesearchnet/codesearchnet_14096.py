def reverse(self):
        """
        Returns a reversed copy of the list.
        """
        colors = ColorList.copy(self)
        _list.reverse(colors)
        return colors