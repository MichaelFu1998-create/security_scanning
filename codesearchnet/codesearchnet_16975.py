def _aggregations_config(self):
        """Load aggregation configurations."""
        result = {}
        for ep in iter_entry_points(
                group=self.entry_point_group_aggs):
            for cfg in ep.load()():
                if cfg['aggregation_name'] not in self.enabled_aggregations:
                    continue
                elif cfg['aggregation_name'] in result:
                    raise DuplicateAggregationError(
                        'Duplicate aggregation {0} in entry point '
                        '{1}'.format(cfg['event_type'], ep.name))
                # Update the default configuration with env/overlay config.
                cfg.update(
                    self.enabled_aggregations[cfg['aggregation_name']] or {}
                )
                result[cfg['aggregation_name']] = cfg
        return result