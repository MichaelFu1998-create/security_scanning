def max_stop(self):
        """
        :returns: maximum stop in list or None if there's at least one open range
        :type: int, float or None
        """
        m = 0
        for r in self:
            if r.is_open():
                return None
            m = max(m, r.stop)
        return m