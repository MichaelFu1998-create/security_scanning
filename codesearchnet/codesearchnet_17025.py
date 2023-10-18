def run(self, start_date=None, end_date=None, **kwargs):
        """Run the query."""
        start_date = self.extract_date(start_date) if start_date else None
        end_date = self.extract_date(end_date) if end_date else None
        self.validate_arguments(start_date, end_date, **kwargs)

        agg_query = self.build_query(start_date, end_date, **kwargs)
        query_result = agg_query.execute().to_dict()
        res = self.process_query_result(query_result, start_date, end_date)
        return res