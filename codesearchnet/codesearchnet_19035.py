def check_ranges(cls, ranges, length):
        """Removes errored ranges"""
        result = []
        for start, end in ranges:
            if isinstance(start, int) or isinstance(end, int):
                if isinstance(start, int) and not (0 <= start < length):
                    continue
                elif isinstance(start, int) and isinstance(end, int) and not (start <= end):
                    continue
                elif start is None and end == 0:
                    continue
                result.append( (start,end) )
        return result