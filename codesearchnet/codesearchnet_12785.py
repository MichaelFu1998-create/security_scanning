def down(self):
        """
        Move this object down one position.
        """
        self.swap(self.get_ordering_queryset().filter(order__gt=self.order))