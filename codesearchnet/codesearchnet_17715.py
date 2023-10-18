def get_water_heaters(self):
        """
        Return a list of water heater devices.

        Parses the response from the locations endpoint in to a pyeconet.WaterHeater.
        """
        water_heaters = []
        for location in self.locations:
            _location_id = location.get("id")
            for device in location.get("equipment"):
                if device.get("type") == "Water Heater":
                    water_heater_modes = self.api_interface.get_modes(device.get("id"))
                    water_heater_usage = self.api_interface.get_usage(device.get("id"))
                    water_heater = self.api_interface.get_device(device.get("id"))
                    vacations = self.api_interface.get_vacations()
                    device_vacations = []
                    for vacation in vacations:
                        for equipment in vacation.get("participatingEquipment"):
                            if equipment.get("id") == water_heater.get("id"):
                                device_vacations.append(EcoNetVacation(vacation, self.api_interface))
                    water_heaters.append(EcoNetWaterHeater(water_heater, water_heater_modes, water_heater_usage,
                                                           _location_id,
                                                           device_vacations,
                                                           self.api_interface))
        return water_heaters