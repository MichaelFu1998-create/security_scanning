def run(self, start_date=None, end_date=None, update_bookmark=True):
        """Calculate statistics aggregations."""
        # If no events have been indexed there is nothing to aggregate
        if not Index(self.event_index, using=self.client).exists():
            return
        lower_limit = start_date or self.get_bookmark()
        # Stop here if no bookmark could be estimated.
        if lower_limit is None:
            return
        upper_limit = min(
            end_date or datetime.datetime.max,  # ignore if `None`
            datetime.datetime.utcnow().replace(microsecond=0),
            datetime.datetime.combine(
                lower_limit + datetime.timedelta(self.batch_size),
                datetime.datetime.min.time())
        )
        while upper_limit <= datetime.datetime.utcnow():
            self.indices = set()
            self.new_bookmark = upper_limit.strftime(self.doc_id_suffix)
            bulk(self.client,
                 self.agg_iter(lower_limit, upper_limit),
                 stats_only=True,
                 chunk_size=50)
            # Flush all indices which have been modified
            current_search_client.indices.flush(
                index=','.join(self.indices),
                wait_if_ongoing=True
            )
            if update_bookmark:
                self.set_bookmark()
            self.indices = set()
            lower_limit = lower_limit + datetime.timedelta(self.batch_size)
            upper_limit = min(
                end_date or datetime.datetime.max,  # ignore if `None``
                datetime.datetime.utcnow().replace(microsecond=0),
                lower_limit + datetime.timedelta(self.batch_size)
            )
            if lower_limit > upper_limit:
                break