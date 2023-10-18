def list_bookmarks(self, start_date=None, end_date=None, limit=None):
        """List the aggregation's bookmarks."""
        query = Search(
            using=self.client,
            index=self.aggregation_alias,
            doc_type=self.bookmark_doc_type
        ).sort({'date': {'order': 'desc'}})

        range_args = {}
        if start_date:
            range_args['gte'] = self._format_range_dt(
                start_date.replace(microsecond=0))
        if end_date:
            range_args['lte'] = self._format_range_dt(
                end_date.replace(microsecond=0))
        if range_args:
            query = query.filter('range', date=range_args)

        return query[0:limit].execute() if limit else query.scan()