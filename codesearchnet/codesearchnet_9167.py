def get_first_of_week(self):
        """
        Returns an integer representing the first day of the week.

        0 represents Monday, 6 represents Sunday.
        """
        if self.first_of_week is None:
            raise ImproperlyConfigured("%s.first_of_week is required." % self.__class__.__name__)
        if self.first_of_week not in range(7):
            raise ImproperlyConfigured("%s.first_of_week must be an integer between 0 and 6." % self.__class__.__name__)
        return self.first_of_week