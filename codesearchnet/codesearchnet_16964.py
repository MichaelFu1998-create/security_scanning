def agg_iter(self, lower_limit=None, upper_limit=None):
        """Aggregate and return dictionary to be indexed in ES."""
        lower_limit = lower_limit or self.get_bookmark().isoformat()
        upper_limit = upper_limit or (
            datetime.datetime.utcnow().replace(microsecond=0).isoformat())
        aggregation_data = {}

        self.agg_query = Search(using=self.client,
                                index=self.event_index).\
            filter('range', timestamp={
                'gte': self._format_range_dt(lower_limit),
                'lte': self._format_range_dt(upper_limit)})

        # apply query modifiers
        for modifier in self.query_modifiers:
            self.agg_query = modifier(self.agg_query)

        hist = self.agg_query.aggs.bucket(
            'histogram',
            'date_histogram',
            field='timestamp',
            interval=self.aggregation_interval
        )
        terms = hist.bucket(
            'terms', 'terms', field=self.aggregation_field, size=0
        )
        top = terms.metric(
            'top_hit', 'top_hits', size=1, sort={'timestamp': 'desc'}
        )
        for dst, (metric, src, opts) in self.metric_aggregation_fields.items():
            terms.metric(dst, metric, field=src, **opts)

        results = self.agg_query.execute()
        index_name = None
        for interval in results.aggregations['histogram'].buckets:
            interval_date = datetime.datetime.strptime(
                interval['key_as_string'], '%Y-%m-%dT%H:%M:%S')
            for aggregation in interval['terms'].buckets:
                aggregation_data['timestamp'] = interval_date.isoformat()
                aggregation_data[self.aggregation_field] = aggregation['key']
                aggregation_data['count'] = aggregation['doc_count']

                if self.metric_aggregation_fields:
                    for f in self.metric_aggregation_fields:
                        aggregation_data[f] = aggregation[f]['value']

                doc = aggregation.top_hit.hits.hits[0]['_source']
                for destination, source in self.copy_fields.items():
                    if isinstance(source, six.string_types):
                        aggregation_data[destination] = doc[source]
                    else:
                        aggregation_data[destination] = source(
                            doc,
                            aggregation_data
                        )

                index_name = 'stats-{0}-{1}'.\
                             format(self.event,
                                    interval_date.strftime(
                                        self.index_name_suffix))
                self.indices.add(index_name)
                yield dict(_id='{0}-{1}'.
                           format(aggregation['key'],
                                  interval_date.strftime(
                                      self.doc_id_suffix)),
                           _index=index_name,
                           _type=self.aggregation_doc_type,
                           _source=aggregation_data)
        self.last_index_written = index_name