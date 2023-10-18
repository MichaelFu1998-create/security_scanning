def schemaforms(self):
        """Load deposit schema forms."""
        _schemaforms = {
            k: v['schemaform']
            for k, v in self.app.config['DEPOSIT_RECORDS_UI_ENDPOINTS'].items()
            if 'schemaform' in v
        }
        return defaultdict(
            lambda: self.app.config['DEPOSIT_DEFAULT_SCHEMAFORM'], _schemaforms
        )