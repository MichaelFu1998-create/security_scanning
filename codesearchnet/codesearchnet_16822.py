def jsonschemas(self):
        """Load deposit JSON schemas."""
        _jsonschemas = {
            k: v['jsonschema']
            for k, v in self.app.config['DEPOSIT_RECORDS_UI_ENDPOINTS'].items()
            if 'jsonschema' in v
        }
        return defaultdict(
            lambda: self.app.config['DEPOSIT_DEFAULT_JSONSCHEMA'], _jsonschemas
        )