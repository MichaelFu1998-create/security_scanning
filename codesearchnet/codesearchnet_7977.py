def _generate_ranges(start_date, end_date):
        """
        Generate a list of 2 month ranges for the range requested with an
        intersection between months. This is necessary because we can't search
        for ranges longer than 3 months and the period searched has to encompass
        the whole period of the mission.
        """
        range_start = start_date
        while range_start < end_date:
            range_end = range_start + timedelta(days=60)
            yield (
                range_start.strftime("%d/%m/%Y"),
                range_end.strftime("%d/%m/%Y")
            )
            range_start += timedelta(days=30)