def build_query(self, interval, start_date, end_date, **kwargs):
        """Build the elasticsearch query."""
        agg_query = Search(using=self.client,
                           index=self.index,
                           doc_type=self.doc_type)[0:0]
        if start_date is not None or end_date is not None:
            time_range = {}
            if start_date is not None:
                time_range['gte'] = start_date.isoformat()
            if end_date is not None:
                time_range['lte'] = end_date.isoformat()
            agg_query = agg_query.filter(
                'range',
                **{self.time_field: time_range})

        for modifier in self.query_modifiers:
            agg_query = modifier(agg_query, **kwargs)

        base_agg = agg_query.aggs.bucket(
            'histogram',
            'date_histogram',
            field=self.time_field,
            interval=interval
        )

        for destination, (metric, field, opts) in self.metric_fields.items():
            base_agg.metric(destination, metric, field=field, **opts)

        if self.copy_fields:
            base_agg.metric(
                'top_hit', 'top_hits', size=1, sort={'timestamp': 'desc'}
            )

        for query_param, filtered_field in self.required_filters.items():
            if query_param in kwargs:
                agg_query = agg_query.filter(
                    'term', **{filtered_field: kwargs[query_param]}
                )

        return agg_query