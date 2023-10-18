def get_temperature(self, format='celsius', sensor=0):
        """
        Get device temperature reading.
        """
        results = self.get_temperatures(sensors=[sensor,])

        if format == 'celsius':
            return results[sensor]['temperature_c']
        elif format == 'fahrenheit':
            return results[sensor]['temperature_f']
        elif format == 'millicelsius':
            return results[sensor]['temperature_mc']
        else:
            raise ValueError("Unknown format")