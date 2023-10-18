def set_target_celsius(self, celsius, mode=config.SCHEDULE_HOLD):
        """
        Set the target temperature to the desired celsius, with more granular control of the hold
        mode

        :param celsius: The desired temperature in C
        :param mode: The desired mode to operate in
        """
        temperature = celsius_to_nuheat(celsius)
        self.set_target_temperature(temperature, mode)