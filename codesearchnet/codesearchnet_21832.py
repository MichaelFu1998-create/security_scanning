def _tosubslices(self, sl):
        """Maps a slice object for whole array to slice objects for subarrays.
        Returns pair (ss, ms) where ss is a list of subarrays and ms is a list
        giving the slice object that should be applied to each subarray.
        """
        N = self.shape[self._distaxis]
        start, stop, step = sl.start, sl.stop, sl.step
        if step is None:
            step = 1
        ss = []
        ms = []
        if step > 0:
            if start is None:
                start = 0
            if stop is None:
                stop = N
            subs = range(0, self._n)
            for s in subs:
                low = self._si[s]
                high = self._si[s + 1]
                first = low + ((low - start) % step)
                last = high + ((high - start) % step)
                if start < high and stop > low and first < high:
                    ss.append(s)
                    substart = max(first, start) - low
                    substop = min(last, stop) - low
                    ms.append(slice(substart, substop, step))
        elif step < 0:
            if start is None:
                start = N - 1
            if stop is None:
                stop = -1
            subs = range(self._n - 1, -1, -1)
            for s in subs:
                low = self._si[s]
                high = self._si[s + 1]
                first = high + step + ((high - start) % step)
                last = low + step + ((low - start) % step)
                if start >= low and stop < high and first >= low:
                    ss.append(s)
                    substart = min(first, start) - low
                    substop = max(last + step, stop) - low
                    if substop < 0:
                        substop = None
                    ms.append(slice(substart, substop, step))
        else:
            raise ValueError('slice step cannot be zero')
        return ss, ms