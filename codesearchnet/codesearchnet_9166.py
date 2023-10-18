def get_end_date(self, obj):
        """
        Returns the end date for a model instance
        """
        obj_date = getattr(obj, self.get_end_date_field())
        try:
            obj_date = obj_date.date()
        except AttributeError:
            # It's a date rather than datetime, so we use it as is
            pass
        return obj_date