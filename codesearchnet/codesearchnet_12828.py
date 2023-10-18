def _subsample(self):
        """ returns a subsample of unlinked snp sites """
        spans = self.maparr
        samp = np.zeros(spans.shape[0], dtype=np.uint64)
        for i in xrange(spans.shape[0]):
            samp[i] = np.random.randint(spans[i, 0], spans[i, 1], 1)
        return samp