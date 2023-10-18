def __serial_transform(self, jam, steps):
        '''A serial transformation union'''
        # This uses the round-robin itertools recipe

        if six.PY2:
            attr = 'next'
        else:
            attr = '__next__'

        pending = len(steps)
        nexts = itertools.cycle(getattr(iter(D.transform(jam)), attr)
                                for (name, D) in steps)

        while pending:
            try:
                for next_jam in nexts:
                    yield next_jam()
            except StopIteration:
                pending -= 1
                nexts = itertools.cycle(itertools.islice(nexts, pending))