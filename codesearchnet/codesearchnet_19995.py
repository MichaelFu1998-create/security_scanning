def _unique(self, sequence, idfun=repr):
        """
        Note: repr() must be implemented properly on all objects. This
        is implicitly assumed by Lancet when Python objects need to be
        formatted to string representation.
        """
        seen = {}
        return [seen.setdefault(idfun(e),e) for e in sequence
                if idfun(e) not in seen]