def bottom(self):
        """
        Move this object to the bottom of the ordered stack.
        """
        o = self.get_ordering_queryset().aggregate(Max('order')).get('order__max')
        self.to(o)