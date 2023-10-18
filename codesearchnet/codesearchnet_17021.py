def process_query_result(self, query_result, interval,
                             start_date, end_date):
        """Build the result using the query result."""
        def build_buckets(agg):
            """Build recursively result buckets."""
            bucket_result = dict(
                key=agg['key'],
                date=agg['key_as_string'],
            )
            for metric in self.metric_fields:
                bucket_result[metric] = agg[metric]['value']
            if self.copy_fields and agg['top_hit']['hits']['hits']:
                doc = agg['top_hit']['hits']['hits'][0]['_source']
                for destination, source in self.copy_fields.items():
                    if isinstance(source, six.string_types):
                        bucket_result[destination] = doc[source]
                    else:
                        bucket_result[destination] = source(bucket_result, doc)
            return bucket_result

        # Add copy_fields
        buckets = query_result['aggregations']['histogram']['buckets']
        return dict(
            interval=interval,
            key_type='date',
            start_date=start_date.isoformat() if start_date else None,
            end_date=end_date.isoformat() if end_date else None,
            buckets=[build_buckets(b) for b in buckets]
        )