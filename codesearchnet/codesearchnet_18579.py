def append(self, next):
        """Append next object to pipe tail.

        :param next: The Pipe object to be appended to tail.
        :type next: Pipe object.
        """
        next.chained = True
        if self.next:
            self.next.append(next)
        else:
            self.next = next