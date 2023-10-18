def _queries_config(self):
        """Load queries configuration."""
        result = {}
        for ep in iter_entry_points(group=self.entry_point_group_queries):
            for cfg in ep.load()():
                if cfg['query_name'] not in self.enabled_queries:
                    continue
                elif cfg['query_name'] in result:
                    raise DuplicateQueryError(
                        'Duplicate query {0} in entry point '
                        '{1}'.format(cfg['query'], ep.name))
                # Update the default configuration with env/overlay config.
                cfg.update(
                    self.enabled_queries[cfg['query_name']] or {}
                )
                result[cfg['query_name']] = cfg
        return result