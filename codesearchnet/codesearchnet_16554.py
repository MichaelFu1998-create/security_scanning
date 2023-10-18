def get_homes(self, only_active=True):
        """Return list of Tibber homes."""
        return [self.get_home(home_id) for home_id in self.get_home_ids(only_active)]