def get_datetime_at_period_ix(self, ix):
        """
        Get the datetime at a given period.

        :param period: The index of the period.

        :returns: The datetime.
        """

        if self.timestep_period_duration == TimePeriod.millisecond:
            return self.start_datetime + timedelta(milliseconds=ix)
        elif self.timestep_period_duration == TimePeriod.second:
            return self.start_datetime + timedelta(seconds=ix)
        elif self.timestep_period_duration == TimePeriod.minute:
            return self.start_datetime + timedelta(minutes=ix)
        elif self.timestep_period_duration == TimePeriod.hour:
            return self.start_datetime + timedelta(hours=ix)
        elif self.timestep_period_duration == TimePeriod.day:
            return self.start_datetime + relativedelta(days=ix)
        elif self.timestep_period_duration == TimePeriod.week:
            return self.start_datetime + relativedelta(days=ix*7)
        elif self.timestep_period_duration == TimePeriod.month:
            return self.start_datetime + relativedelta(months=ix)
        elif self.timestep_period_duration == TimePeriod.year:
            return self.start_datetime + relativedelta(years=ix)