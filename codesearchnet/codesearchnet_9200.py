def get_humidity(self, sensors=None):
        """
        Get device humidity reading.

        Params:
        - sensors: optional list of sensors to get a reading for, examples:
          [0,] - get reading for sensor 0
          [0, 1,] - get reading for sensors 0 and 1
          None - get readings for all sensors
        """
        _sensors = sensors
        if _sensors is None:
            _sensors = list(range(0, self._sensor_count))

        if not set(_sensors).issubset(list(range(0, self._sensor_count))):
            raise ValueError(
                'Some or all of the sensors in the list %s are out of range '
                'given a sensor_count of %d.  Valid range: %s' % (
                    _sensors,
                    self._sensor_count,
                    list(range(0, self._sensor_count)),
                )
            )

        data = self.get_data()
        data = data['humidity_data']

        results = {}

        # Interpret device response
        for sensor in _sensors:
            offset = self.lookup_humidity_offset(sensor)
            if offset is None:
                continue
            humidity = (struct.unpack_from('>H', data, offset)[0] * 32) / 1000.0
            results[sensor] = {
                'ports': self.get_ports(),
                'bus': self.get_bus(),
                'sensor': sensor,
                'humidity_pc': humidity,
            }

        return results