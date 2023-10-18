def set_target_temperature(self, temperature, mode=config.SCHEDULE_HOLD):
        """
        Updates the target temperature on the NuHeat API

        :param temperature: The desired temperature in NuHeat format
        :param permanent: Permanently hold the temperature. If set to False, the schedule will
                          resume at the next programmed event
        """
        if temperature < self.min_temperature:
            temperature = self.min_temperature

        if temperature > self.max_temperature:
            temperature = self.max_temperature

        modes = [config.SCHEDULE_TEMPORARY_HOLD, config.SCHEDULE_HOLD]
        if mode not in modes:
            raise Exception("Invalid mode. Please use one of: {}".format(modes))

        self.set_data({
            "SetPointTemp": temperature,
            "ScheduleMode": mode
        })