def recently_ended(self):
        """
        Determines if event ended recently (within 5 days).
        Useful for attending list.
        """
        if self.ended():
            end_date = self.end_date if self.end_date else self.start_date
            if end_date >= offset.date():
                return True