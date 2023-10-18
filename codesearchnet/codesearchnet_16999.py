def run(self):
        """Process events queue."""
        return elasticsearch.helpers.bulk(
            self.client,
            self.actionsiter(),
            stats_only=True,
            chunk_size=50
        )