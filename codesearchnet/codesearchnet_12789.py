def top(self):
        """
        Move this object to the top of the ordered stack.
        """
        o = self.get_ordering_queryset().aggregate(Min('order')).get('order__min')
        self.to(o)