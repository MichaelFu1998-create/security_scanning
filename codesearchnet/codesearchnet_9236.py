def retain_identities(self, retention_time):
        """Retain the identities in SortingHat based on the `retention_time`
        value declared in the setup.cfg.

        :param retention_time: maximum number of minutes wrt the current date to retain the SortingHat data
        """
        enrich_es = self.conf['es_enrichment']['url']
        sortinghat_db = self.db
        current_data_source = self.get_backend(self.backend_section)
        active_data_sources = self.config.get_active_data_sources()

        if retention_time is None:
            logger.debug("[identities retention] Retention policy disabled, no identities will be deleted.")
            return

        if retention_time <= 0:
            logger.debug("[identities retention] Retention time must be greater than 0.")
            return

        retain_identities(retention_time, enrich_es, sortinghat_db, current_data_source, active_data_sources)