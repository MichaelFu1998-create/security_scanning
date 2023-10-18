def show(self, exclude=[]):
        """
        Convenience method to inspect the available argument values in
        human-readable format. The ordering of keys is determined by
        how quickly they vary.

        The exclude list allows specific keys to be excluded for
        readability (e.g. to hide long, absolute filenames).
        """
        ordering = self.constant_keys + self.varying_keys
        spec_lines = [', '.join(['%s=%s' % (k, s[k]) for k in ordering
                                 if (k in s) and (k not in exclude)])
                      for s in self.specs]
        print('\n'.join(['%d: %s' % (i,l) for (i,l) in enumerate(spec_lines)]))