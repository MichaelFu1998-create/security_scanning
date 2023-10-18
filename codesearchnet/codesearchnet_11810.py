def has_changes(self):
        """
        Returns true if at least one tracker detects a change.
        """
        lm = self.last_manifest
        for tracker in self.get_trackers():
            last_thumbprint = lm['_tracker_%s' % tracker.get_natural_key_hash()]
            if tracker.is_changed(last_thumbprint):
                return True
        return False