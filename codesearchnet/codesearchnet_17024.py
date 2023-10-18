def process_query_result(self, query_result, start_date, end_date):
        """Build the result using the query result."""
        def build_buckets(agg, fields, bucket_result):
            """Build recursively result buckets."""
            # Add metric results for current bucket
            for metric in self.metric_fields:
                bucket_result[metric] = agg[metric]['value']
            if fields:
                current_level = fields[0]
                bucket_result.update(dict(
                    type='bucket',
                    field=current_level,
                    key_type='terms',
                    buckets=[build_buckets(b, fields[1:], dict(key=b['key']))
                             for b in agg[current_level]['buckets']]
                ))
            return bucket_result

        # Add copy_fields
        aggs = query_result['aggregations']
        result = dict(
            start_date=start_date.isoformat() if start_date else None,
            end_date=end_date.isoformat() if end_date else None,
        )
        if self.copy_fields and aggs['top_hit']['hits']['hits']:
            doc = aggs['top_hit']['hits']['hits'][0]['_source']
            for destination, source in self.copy_fields.items():
                if isinstance(source, six.string_types):
                    result[destination] = doc[source]
                else:
                    result[destination] = source(result, doc)

        return build_buckets(aggs, self.aggregated_fields, result)