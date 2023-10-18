def read_from(self, data, pad=0):
        """
        Returns a generator with the elements "data" taken by offset, restricted
        by self.begin and self.end, and padded on either end by `pad` to get
        back to the original length of `data`
        """
        for i in range(self.BEGIN, self.END + 1):
            index = self.index(i, len(data))
            yield pad if index is None else data[index]