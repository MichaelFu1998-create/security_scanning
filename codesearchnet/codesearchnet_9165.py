def get_start_date(self, obj):
        """
        Returns the start date for a model instance
        """
        obj_date = getattr(obj, self.get_date_field())
        try:
            obj_date = obj_date.date()
        except AttributeError:
            # It's a date rather than datetime, so we use it as is
            pass
        return obj_date