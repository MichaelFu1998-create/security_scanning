def write(self, data):
        """
        Writes the symbolic bytes in C{data} onto the file.
        """
        size = min(len(data), self.max_size - self.pos)
        for i in range(self.pos, self.pos + size):
            self.array[i] = data[i - self.pos]