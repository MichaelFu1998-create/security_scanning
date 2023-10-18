def _cmp(self, other):
        """
        Compare two Project Haystack version strings, then return
            -1 if self < other,
            0 if self == other
            or 1 if self > other.
        """
        if not isinstance(other, Version):
            other = Version(other)

        num1 = self.version_nums
        num2 = other.version_nums

        # Pad both to be the same length
        ver_len = max(len(num1), len(num2))
        num1 += tuple([0 for n in range(len(num1), ver_len)])
        num2 += tuple([0 for n in range(len(num2), ver_len)])

        # Compare the versions
        for (p1, p2) in zip(num1, num2):
            if p1 < p2:
                return -1
            elif p1 > p2:
                return 1

        # All the same, compare the extra strings.
        # If a version misses the extra part; we consider that as coming *before*.
        if self.version_extra is None:
            if other.version_extra is None:
                return 0
            else:
                return -1
        elif other.version_extra is None:
            return 1
        elif self.version_extra == other.version_extra:
            return 0
        elif self.version_extra < other.version_extra:
            return -1
        else:
            return 1