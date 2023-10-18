def get_lights(self):
        """Get current light data, set and return as list of Bulb objects."""
        # Throttle updates. Use cached data if within UPDATE_INTERVAL_SECONDS
        now = datetime.datetime.now()
        if (now - self._last_updated) < datetime.timedelta(
                seconds=UPDATE_INTERVAL_SECONDS):
            # _LOGGER.debug("Using cached light data")
            return self._bulbs
        else:
            self._last_updated = now

        light_data = self.get_data()
        _LOGGER.debug("got: %s", light_data)
        if not light_data:
            return []

        if self._bulbs:
            # Bulbs already created, just update values
            for bulb in self._bulbs:
                # use the values for the bulb with the correct ID
                try:
                    values = light_data[bulb.zid]
                    bulb._online, bulb._red, bulb._green, bulb._blue, \
                        bulb._level = values
                except KeyError:
                    pass
        else:
            for light_id in light_data:
                self._bulbs.append(Bulb(self, light_id, *light_data[light_id]))
        # return a list of Bulb objects
        return self._bulbs