def condense_ranges(cls, ranges):
        """Sorts and removes overlaps"""
        result = []
        if ranges:
            ranges.sort(key=lambda tup: tup[0])
            result.append(ranges[0])
            for i in range(1, len(ranges)):
                if result[-1][1] + 1 >= ranges[i][0]:
                    result[-1] = (result[-1][0], max(result[-1][1], ranges[i][1]))
                else:
                    result.append(ranges[i])
        return result