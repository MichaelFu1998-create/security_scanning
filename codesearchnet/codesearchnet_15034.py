def upload(self, docs_base, release):
        """Upload docs in ``docs_base`` to the target of this uploader."""
        return getattr(self, '_to_' + self.target)(docs_base, release)