def sync(self):
        """
        Fetch the list of apps from Marathon, find the domains that require
        certificates, and issue certificates for any domains that don't already
        have a certificate.
        """
        self.log.info('Starting a sync...')

        def log_success(result):
            self.log.info('Sync completed successfully')
            return result

        def log_failure(failure):
            self.log.failure('Sync failed', failure, LogLevel.error)
            return failure

        return (self.marathon_client.get_apps()
                .addCallback(self._apps_acme_domains)
                .addCallback(self._filter_new_domains)
                .addCallback(self._issue_certs)
                .addCallbacks(log_success, log_failure))