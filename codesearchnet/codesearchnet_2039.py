def fast_search(self, pattern_codes):
        """Skips forward in a string as fast as possible using information from
        an optimization info block."""
        # pattern starts with a known prefix
        # <5=length> <6=skip> <7=prefix data> <overlap data>
        flags = pattern_codes[2]
        prefix_len = pattern_codes[5]
        prefix_skip = pattern_codes[6] # don't really know what this is good for
        prefix = pattern_codes[7:7 + prefix_len]
        overlap = pattern_codes[7 + prefix_len - 1:pattern_codes[1] + 1]
        pattern_codes = pattern_codes[pattern_codes[1] + 1:]
        i = 0
        string_position = self.string_position
        while string_position < self.end:
            while True:
                if ord(self.string[string_position]) != prefix[i]:
                    if i == 0:
                        break
                    else:
                        i = overlap[i]
                else:
                    i += 1
                    if i == prefix_len:
                        # found a potential match
                        self.start = string_position + 1 - prefix_len
                        self.string_position = string_position + 1 \
                                                     - prefix_len + prefix_skip
                        if flags & SRE_INFO_LITERAL:
                            return True # matched all of pure literal pattern
                        if self.match(pattern_codes[2 * prefix_skip:]):
                            return True
                        i = overlap[i]
                    break
            string_position += 1
        return False