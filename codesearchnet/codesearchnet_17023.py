def build_query(self, start_date, end_date, **kwargs):
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

        base_agg = agg_query.aggs

        def _apply_metric_aggs(agg):
            for dst, (metric, field, opts) in self.metric_fields.items():
                agg.metric(dst, metric, field=field, **opts)

        _apply_metric_aggs(base_agg)
        if self.aggregated_fields:
            cur_agg = base_agg
            for term in self.aggregated_fields:
                cur_agg = cur_agg.bucket(term, 'terms', field=term, size=0)
                _apply_metric_aggs(cur_agg)

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