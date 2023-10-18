def get_components(self, line, with_type=True):
        """Return a dict of components in the line.

        key: device name (ex: 'sdc1')
        value: device role number
        """
        ret = {}

        # Ignore (F) (see test 08)
        line2 = reduce(lambda x, y: x + y, split('\(.+\)', line))
        if with_type:
            splitted = split('\W+', line2)[3:]
        else:
            splitted = split('\W+', line2)[2:]
        ret = dict(zip(splitted[0::2], splitted[1::2]))

        return ret