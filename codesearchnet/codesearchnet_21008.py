def to_date(self):
        """
        construct datetime.date instance represented calendar date of BusinessDate instance

        :return datetime.date:
        """
        y, m, d = self.to_ymd()
        return date(y, m, d)