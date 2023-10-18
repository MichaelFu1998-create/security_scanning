def _expand_pattern(self, pattern):
        """
        From the pattern decomposition, finds the absolute paths
        matching the pattern.
        """
        (globpattern, regexp, fields, types) = self._decompose_pattern(pattern)
        filelist = glob.glob(globpattern)
        expansion = []

        for fname in filelist:
            if fields == []:
                expansion.append((fname, {}))
                continue
            match = re.match(regexp, fname)
            if match is None: continue
            match_items = match.groupdict().items()
            tags = dict((k,types.get(k, str)(v)) for (k,v) in match_items)
            expansion.append((fname, tags))

        return expansion