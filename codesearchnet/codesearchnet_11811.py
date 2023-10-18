def configure(self):
        """
        The standard method called to apply functionality when the manifest changes.
        """
        lm = self.last_manifest
        for tracker in self.get_trackers():
            self.vprint('Checking tracker:', tracker)
            last_thumbprint = lm['_tracker_%s' % tracker.get_natural_key_hash()]
            self.vprint('last thumbprint:', last_thumbprint)
            has_changed = tracker.is_changed(last_thumbprint)
            self.vprint('Tracker changed:', has_changed)
            if has_changed:
                self.vprint('Change detected!')
                tracker.act()