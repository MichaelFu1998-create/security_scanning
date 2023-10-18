def waitForFocusToMatchCriteria(self, timeout=10, **kwargs):
        """Convenience method to wait for focused element to change
        (to element matching kwargs criteria).

        Returns: Element or None

        """

        def _matchFocused(retelem, **kwargs):
            return retelem if retelem._match(**kwargs) else None

        retelem = None
        return self._waitFor(timeout, 'AXFocusedUIElementChanged',
                             callback=_matchFocused,
                             args=(retelem,),
                             **kwargs)