def record_manifest(self):
        """
        Called after a deployment to record any data necessary to detect changes
        for a future deployment.
        """
        manifest = super(ApacheSatchel, self).record_manifest()
        manifest['available_sites'] = self.genv.available_sites
        manifest['available_sites_by_host'] = self.genv.available_sites_by_host
        manifest['media_timestamp'] = self.get_media_timestamp()
        return manifest