def iter(self, prev=None):
        """Return an generator as iterator object.

        :param prev: Previous Pipe object which used for data input.
        :returns: A generator for iteration.
        """

        if self.next:
            generator = self.next.iter(self.func(prev, *self.args, **self.kw))
        else:
            generator = self.func(prev, *self.args, **self.kw)
        return generator