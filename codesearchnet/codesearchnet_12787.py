def above(self, ref):
        """
        Move this object above the referenced object.
        """
        if not self._valid_ordering_reference(ref):
            raise ValueError(
                "%r can only be moved above instances of %r which %s equals %r." % (
                    self, self.__class__, self.order_with_respect_to,
                    self._get_order_with_respect_to()
                )
            )
        if self.order == ref.order:
            return
        if self.order > ref.order:
            o = ref.order
        else:
            o = self.get_ordering_queryset().filter(order__lt=ref.order).aggregate(Max('order')).get('order__max') or 0
        self.to(o)