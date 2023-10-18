def set_data(self, post_data):
        """
        Update (patch) the current instance's data on the NuHeat API
        """
        params = {
            "serialnumber": self.serial_number
        }
        self._session.request(config.THERMOSTAT_URL, method="POST", data=post_data, params=params)