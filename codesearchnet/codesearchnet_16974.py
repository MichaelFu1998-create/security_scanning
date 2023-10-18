def _events_config(self):
        """Load events configuration."""
        # import iter_entry_points here so that it can be mocked in tests
        result = {}
        for ep in iter_entry_points(
                group=self.entry_point_group_events):
            for cfg in ep.load()():
                if cfg['event_type'] not in self.enabled_events:
                    continue
                elif cfg['event_type'] in result:
                    raise DuplicateEventError(
                        'Duplicate event {0} in entry point '
                        '{1}'.format(cfg['event_type'], ep.name))
                # Update the default configuration with env/overlay config.
                cfg.update(
                    self.enabled_events[cfg['event_type']] or {}
                )
                result[cfg['event_type']] = cfg
        return result