def _dump(self, tag, x, lo, hi):
        """Generate comparison results for a same-tagged range."""
        for i in xrange(lo, hi):
            yield '%s %s' % (tag, x[i])