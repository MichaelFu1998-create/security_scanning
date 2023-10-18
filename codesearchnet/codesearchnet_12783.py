def swap(self, qs):
        """
        Swap the positions of this object with a reference object.
        """
        try:
            replacement = qs[0]
        except IndexError:
            # already first/last
            return
        if not self._valid_ordering_reference(replacement):
            raise ValueError(
                "%r can only be swapped with instances of %r which %s equals %r." % (
                    self, self.__class__, self.order_with_respect_to,
                    self._get_order_with_respect_to()
                )
            )
        self.order, replacement.order = replacement.order, self.order
        self.save()
        replacement.save()