def has_overlaps(self):
        """
        :returns: True if one or more range in the list overlaps with another
        :rtype: bool
        """
        sorted_list = sorted(self)
        for i in range(0, len(sorted_list) - 1):
            if sorted_list[i].overlaps(sorted_list[i + 1]):
                return True
        return False