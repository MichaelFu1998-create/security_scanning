def mappings(self):
        """
        Returns a sorted list of all the mappings for this memory.

        :return: a list of mappings.
        :rtype: list
        """
        result = []
        for m in self.maps:
            if isinstance(m, AnonMap):
                result.append((m.start, m.end, m.perms, 0, ''))
            elif isinstance(m, FileMap):
                result.append((m.start, m.end, m.perms, m._offset, m._filename))
            else:
                result.append((m.start, m.end, m.perms, 0, m.name))

        return sorted(result)