def from_element(root, timezone):
        """Return a Schedule object based on an lxml Element for the <schedule>
        tag. timezone is a tzinfo object, ideally from pytz."""
        assert root.tag == 'schedule'
        if root.xpath('intervals'):
            return _ScheduleIntervals(root, timezone)
        elif root.xpath('recurring_schedules'):
            return _ScheduleRecurring(root, timezone)
        raise NotImplementedError