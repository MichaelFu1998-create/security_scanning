def is_expired(self):
        """
        Determine if the confirmation has expired.

        Returns:
            bool:
                ``True`` if the confirmation has expired and ``False``
                otherwise.
        """
        expiration_time = self.created_at + datetime.timedelta(days=1)

        return timezone.now() > expiration_time