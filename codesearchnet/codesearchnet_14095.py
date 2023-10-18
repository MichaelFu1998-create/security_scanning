def cluster_sort(self, cmp1="hue", cmp2="brightness", reversed=False, n=12):
        """
        Sorts the list by cmp1, then cuts it into n pieces which are sorted by cmp2.

        If you want to cluster by hue, use n=12 (since there are 12 primary/secondary hues).
        The resulting list will not contain n even slices:
        n is used rather to slice up the cmp1 property of the colors,
        e.g. cmp1=brightness and n=3 will cluster colors by brightness >= 0.66, 0.33, 0.0
        """
        sorted = self.sort(cmp1)
        clusters = ColorList()

        d = 1.0
        i = 0
        for j in _range(len(sorted)):
            if getattr(sorted[j], cmp1) < d:
                clusters.extend(sorted[i:j].sort(cmp2))
                d -= 1.0 / n
                i = j
        clusters.extend(sorted[i:].sort(cmp2))
        if reversed: _list.reverse(clusters)
        return clusters