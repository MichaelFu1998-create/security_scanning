def below(self, ref):
        """
        Move this object below the referenced object.
        """
        if not self._valid_ordering_reference(ref):
            raise ValueError(
                "%r can only be moved below instances of %r which %s equals %r." % (
                    self, self.__class__, self.order_with_respect_to,
                    self._get_order_with_respect_to()
                )
            )
        if self.order == ref.order:
            return
        if self.order > ref.order:
            o = self.get_ordering_queryset().filter(order__gt=ref.order).aggregate(Min('order')).get('order__min') or 0
        else:
            o = ref.order
        self.to(o)