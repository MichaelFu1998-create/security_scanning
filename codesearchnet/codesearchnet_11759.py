def record_manifest(self):
        """
        Called after a deployment to record any data necessary to detect changes
        for a future deployment.
        """
        manifest = super(PIPSatchel, self).record_manifest()
        manifest['all-requirements'] = self.get_combined_requirements()
        if self.verbose:
            pprint(manifest, indent=4)
        return manifest