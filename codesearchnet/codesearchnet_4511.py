def status(self):
        """Returns the status of the executor via probing the execution providers."""
        if self.provider:
            status = self.provider.status(self.engines)

        else:
            status = []

        return status