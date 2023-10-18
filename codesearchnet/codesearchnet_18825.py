def get_date(self, filename):
        """Return the date of the article in file."""
        try:
            self.document = parse(filename)
            return self._get_date()
        except DateNotFoundException:
            print("Date problem found in {0}".format(filename))
            return datetime.datetime.strftime(datetime.datetime.now(),
                                              "%Y-%m-%d")