def to_timezone(self, dt):
        """Converts a datetime to the timezone of this Schedule."""
        if timezone.is_aware(dt):
            return dt.astimezone(self.timezone)
        else:
            return timezone.make_aware(dt, self.timezone)