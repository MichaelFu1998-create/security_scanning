def record_manifest(self):
        """
        Called after a deployment to record any data necessary to detect changes
        for a future deployment.
        """
        manifest = super(GitTrackerSatchel, self).record_manifest()
        manifest[CURRENT_COMMIT] = self.get_current_commit()
        return manifest