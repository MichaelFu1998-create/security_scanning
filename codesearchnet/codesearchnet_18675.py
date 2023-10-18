def set_target_fahrenheit(self, fahrenheit, mode=config.SCHEDULE_HOLD):
        """
        Set the target temperature to the desired fahrenheit, with more granular control of the
        hold mode

        :param fahrenheit: The desired temperature in F
        :param mode: The desired mode to operate in
        """
        temperature = fahrenheit_to_nuheat(fahrenheit)
        self.set_target_temperature(temperature, mode)