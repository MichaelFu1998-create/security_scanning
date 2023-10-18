def get_data(self):
        """
        Fetch/refresh the current instance's data from the NuHeat API
        """
        params = {
            "serialnumber": self.serial_number
        }
        data = self._session.request(config.THERMOSTAT_URL, params=params)

        self._data = data

        self.heating = data.get("Heating")
        self.online = data.get("Online")
        self.room = data.get("Room")
        self.serial_number = data.get("SerialNumber")
        self.temperature = data.get("Temperature")
        self.min_temperature = data.get("MinTemp")
        self.max_temperature = data.get("MaxTemp")
        self.target_temperature = data.get("SetPointTemp")
        self._schedule_mode = data.get("ScheduleMode")