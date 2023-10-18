def status(self):
        """Return status of all blocks."""

        status = []
        if self.provider:
            status = self.provider.status(self.blocks.values())

        return status