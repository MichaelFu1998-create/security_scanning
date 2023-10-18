def fetch_and_filter_tags(self):
        """
        Fetch and filter tags, fetch dates and sort them in time order.
        """

        self.all_tags = self.fetcher.get_all_tags()
        self.filtered_tags = self.get_filtered_tags(self.all_tags)
        self.fetch_tags_dates()