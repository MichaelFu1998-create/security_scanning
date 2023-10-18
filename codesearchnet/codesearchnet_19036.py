def convert_ranges(cls, ranges, length):
        """Converts to valid byte ranges"""
        result = []
        for start, end in ranges:
            if end is None:
                result.append( (start, length-1) )
            elif start is None:
                s = length - end
                result.append( (0 if s < 0 else s, length-1) )
            else:
                result.append( (start, end if end < length else length-1) )
        return result