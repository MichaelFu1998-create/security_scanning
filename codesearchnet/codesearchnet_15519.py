def process(self, expression):
        """ Process color expression
        args:
            expression (tuple): color expression
        returns:
            str
        """
        a, o, b = expression
        c1 = self._hextorgb(a)
        c2 = self._hextorgb(b)
        r = ['#']
        for i in range(3):
            v = self.operate(c1[i], c2[i], o)
            if v > 0xff:
                v = 0xff
            if v < 0:
                v = 0
            r.append("%02x" % int(v))
        return ''.join(r)