def is_locked(self):
        """Return True, if URI is locked."""
        if self.provider.lock_manager is None:
            return False
        return self.provider.lock_manager.is_url_locked(self.get_ref_url())