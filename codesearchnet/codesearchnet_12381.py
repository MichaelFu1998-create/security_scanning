def _convert_item(self, obj):
        """
        Convert obj into a DotDict, or list of DotDict.

        Directly nested lists aren't supported.
        Returns the result
        """
        if isinstance(obj, dict) and not isinstance(obj, DotDict):
            obj = DotDict(obj)
        elif isinstance(obj, list):
            # must mutate and not just reassign, otherwise it will
            # just use original object mutable/immutable
            for i, item in enumerate(obj):
                if isinstance(item, dict) and not isinstance(item, DotDict):
                    obj[i] = DotDict(item)
        return obj