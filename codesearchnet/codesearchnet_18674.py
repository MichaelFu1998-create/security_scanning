def schedule_mode(self, mode):
        """
        Set the thermostat mode

        :param mode: The desired mode integer value.
                     Auto = 1
                     Temporary hold = 2
                     Permanent hold = 3
        """
        modes = [config.SCHEDULE_RUN, config.SCHEDULE_TEMPORARY_HOLD, config.SCHEDULE_HOLD]
        if mode not in modes:
            raise Exception("Invalid mode. Please use one of: {}".format(modes))

        self.set_data({"ScheduleMode": mode})