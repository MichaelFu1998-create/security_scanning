def record_manifest(self):
        """
        Called after a deployment to record any data necessary to detect changes
        for a future deployment.
        """
        manifest = super(SeleniumSatchel, self).record_manifest()
        manifest['fingerprint'] = str(self.get_target_geckodriver_version_number())
        return manifest