def read(self, count):
        """
        Reads up to C{count} bytes from the file.
        :rtype: list
        :return: the list of symbolic bytes read
        """
        if self.pos > self.max_size:
            return []
        else:
            size = min(count, self.max_size - self.pos)
            ret = [self.array[i] for i in range(self.pos, self.pos + size)]
            self.pos += size
            return ret