def _characteristics_discovered(self, service):
        """Called when GATT characteristics have been discovered."""
        # Characteristics for the specified service were discovered.  Update
        # set of discovered services and signal when all have been discovered.
        self._discovered_services.add(service)
        if self._discovered_services >= set(self._peripheral.services()):
            # Found all the services characteristics, finally time to fire the
            # service discovery complete event.
            self._discovered.set()