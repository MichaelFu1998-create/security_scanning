def up(self):
        """
        Move this object up one position.
        """
        self.swap(self.get_ordering_queryset().filter(order__lt=self.order).order_by('-order'))