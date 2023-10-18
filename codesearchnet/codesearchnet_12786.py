def to(self, order):
        """
        Move object to a certain position, updating all affected objects to move accordingly up or down.
        """
        if order is None or self.order == order:
            # object is already at desired position
            return
        qs = self.get_ordering_queryset()
        if self.order > order:
            qs.filter(order__lt=self.order, order__gte=order).update(order=F('order') + 1)
        else:
            qs.filter(order__gt=self.order, order__lte=order).update(order=F('order') - 1)
        self.order = order
        self.save()