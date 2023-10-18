def byte_length(self):
        """
        :returns: sum of lengthes of all ranges or None if one of the ranges is open
        :rtype: int, float or None
        """
        sum = 0
        for r in self:
            if r.is_open():
                return None
            sum += r.byte_length()
        return sum