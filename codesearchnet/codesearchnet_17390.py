def _matchOther(self, obj, **kwargs):
        """Perform _match but on another object, not self."""
        if obj is not None:
            # Need to check that the returned UI element wasn't destroyed first:
            if self._findFirstR(**kwargs):
                return obj._match(**kwargs)
        return False