def animation(self):
        """
        :returns: the selected animation based on self.index, or None if
            self.index is out of bounds
        """
        if 0 <= self._index < len(self.animations):
            return self.animations[self._index]