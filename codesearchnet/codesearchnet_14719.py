def daily_at(cls, at, target):
        """
        Schedule a command to run at a specific time each day.
        """
        daily = datetime.timedelta(days=1)
        # convert when to the next datetime matching this time
        when = datetime.datetime.combine(datetime.date.today(), at)
        if when < now():
            when += daily
        return cls.at_time(cls._localize(when), daily, target)