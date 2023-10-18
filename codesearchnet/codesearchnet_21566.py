def daily_periods(self, range_start=datetime.date.min, range_end=datetime.date.max, exclude_dates=tuple()):
        """Returns an iterator of Period tuples for every day this schedule is in effect, between range_start
        and range_end."""
        tz = self.timezone
        period = self.period
        weekdays = self.weekdays

        current_date = max(range_start, self.start_date)
        end_date = range_end
        if self.end_date:
            end_date = min(end_date, self.end_date)

        while current_date <= end_date:
            if current_date.weekday() in weekdays and current_date not in exclude_dates:
                yield Period(
                    tz.localize(datetime.datetime.combine(current_date, period.start)),
                    tz.localize(datetime.datetime.combine(current_date, period.end))
                )
            current_date += datetime.timedelta(days=1)