def cut(self, by, from_start=True):
        """ Cuts this object from_start to the number requestd
        returns new instance
        """
        s, e = copy(self.start), copy(self.end)
        if from_start:
            e = s + by
        else:
            s = e - by
        return Range(s, e)