def exception_periods(self, range_start=datetime.date.min, range_end=datetime.date.max):
        """Returns a list of Period tuples for each period represented in an <exception>
        that falls between range_start and range_end."""
        periods = []
        for exception_date, exception_times in self.exceptions.items():
            if exception_date >= range_start and exception_date <= range_end:
                for exception_time in exception_times:
                    periods.append(
                        Period(
                            self.timezone.localize(datetime.datetime.combine(exception_date, exception_time.start)),
                            self.timezone.localize(datetime.datetime.combine(exception_date, exception_time.end))
                        )
                    )

        periods.sort()
        return periods