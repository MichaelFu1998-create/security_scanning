def get_home(self, home_id):
        """Retun an instance of TibberHome for given home id."""
        if home_id not in self._all_home_ids:
            _LOGGER.error("Could not find any Tibber home with id: %s", home_id)
            return None
        if home_id not in self._homes.keys():
            self._homes[home_id] = TibberHome(home_id, self)
        return self._homes[home_id]