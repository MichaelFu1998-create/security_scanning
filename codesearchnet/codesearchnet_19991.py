def _collect_by_key(self,specs):
        """
        Returns a dictionary like object with the lists of values
        collapsed by their respective key. Useful to find varying vs
        constant keys and to find how fast keys vary.
        """
        # Collect (key, value) tuples as list of lists, flatten with chain
        allkeys = itertools.chain.from_iterable(
            [[(k, run[k]) for k in run] for run in specs])
        collection = defaultdict(list)
        for (k,v) in allkeys: collection[k].append(v)
        return collection