def record_manifest(self):
        """
        Called after a deployment to record any data necessary to detect changes
        for a future deployment.
        """
        manifest = super(TarballSatchel, self).record_manifest()
        manifest['timestamp'] = self.timestamp
        return manifest