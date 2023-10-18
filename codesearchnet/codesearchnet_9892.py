def read(self, count):
        """Read count characters starting at self.index,
        and return those characters as a string
        """
        new_index = self.index + count
        if new_index > self.len:
            buf = self.raw_text[self.index :]  # return to the end, don't fail
        else:
            buf = self.raw_text[self.index : new_index]
        self.index = new_index

        return buf